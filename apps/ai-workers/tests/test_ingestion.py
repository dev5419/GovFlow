"""
Unit tests for GovFlow Ingestion Worker (F-02) per PRD §8.2, §11.2, §11.3.

Acceptance criteria:
- Invalid file types are rejected before processing with clear error result.
- Original documents are stored without modification (verified byte-for-byte).
- Each processed file is linked to its tender/bidder context.
- A document.preprocessed event is published with the correct payload shape.
- Zip-slip path traversal attacks are safely defended.
"""

import io
import os
import zipfile
import pytest
from unittest.mock import MagicMock, patch
from pypdf import PdfWriter
from PIL import Image

from src.ingestion_worker.zip_extractor import safe_extract_zip, ZipExtractionError
from src.ingestion_worker.pdf_splitter import split_pdf, PdfSplitError
from src.ingestion_worker.document_classifier import classify_document
from src.ingestion_worker.image_preprocessor import preprocess_image
from src.queue.consumers.ingestion_consumer import (
    process_document_uploaded_event,
    IngestionError,
)


# ---------------------------------------------------------------------------
# Helper test utilities
# ---------------------------------------------------------------------------

def _create_sample_pdf(num_pages: int = 3, width: int = 595, height: int = 842) -> bytes:
    """Create a minimal valid multi-page PDF in memory using pypdf."""
    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=width, height=height)
    stream = io.BytesIO()
    writer.write(stream)
    return stream.getvalue()


def _create_sample_image(width: int = 600, height: int = 800, color: str = "white") -> bytes:
    """Create a valid PNG image in memory using Pillow."""
    img = Image.new("RGB", (width, height), color=color)
    stream = io.BytesIO()
    img.save(stream, format="PNG")
    return stream.getvalue()


def _create_sample_zip(files_dict: dict) -> bytes:
    """Create a valid in-memory ZIP archive from a dict of {path: bytes}."""
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files_dict.items():
            zf.writestr(name, data)
    return stream.getvalue()


# ---------------------------------------------------------------------------
# 1. ZIP Extractor Tests & Zip-Slip Defense
# ---------------------------------------------------------------------------

class TestZipExtractor:
    def test_safe_zip_extraction(self):
        """Valid ZIP archive with PDF and images extracts correctly with exact byte content."""
        pdf_bytes = _create_sample_pdf(1)
        img_bytes = _create_sample_image()
        zip_data = _create_sample_zip({
            "bid_package/gst_certificate.pdf": pdf_bytes,
            "bid_package/pan_card.png": img_bytes,
        })

        extracted = safe_extract_zip(zip_data)
        assert len(extracted) == 2
        assert {e.file_name for e in extracted} == {"gst_certificate.pdf", "pan_card.png"}

        # Verify byte-for-byte integrity of original files
        for e in extracted:
            if e.file_name == "gst_certificate.pdf":
                assert e.file_bytes == pdf_bytes
                assert e.file_size == len(pdf_bytes)
                assert e.is_supported is True
            elif e.file_name == "pan_card.png":
                assert e.file_bytes == img_bytes
                assert e.file_size == len(img_bytes)
                assert e.is_supported is True

    def test_zip_slip_path_traversal_defense(self):
        """Zip-slip attempts using ../ or relative escapes are blocked with ZipExtractionError."""
        malicious_zip = _create_sample_zip({
            "../../../../etc/passwd.pdf": b"root:x:0:0:root:/root:/bin/bash",
            "..\\..\\windows\\system32\\calc.exe": b"fake executable",
        })

        with pytest.raises(ZipExtractionError) as exc_info:
            safe_extract_zip(malicious_zip)
        assert "path traversal" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# 2. PDF Splitter Tests
# ---------------------------------------------------------------------------

class TestPdfSplitter:
    def test_multipage_pdf_split(self):
        """Splits multipage PDF into per-page records, preserving 1-indexed order and dimensions."""
        pdf_bytes = _create_sample_pdf(num_pages=3, width=612, height=792)
        pages = split_pdf(pdf_bytes)

        assert len(pages) == 3
        for i, page in enumerate(pages):
            assert page.page_number == i + 1
            assert page.page_width == 612
            assert page.page_height == 792
            assert len(page.page_bytes) > 0


# ---------------------------------------------------------------------------
# 3. Document Classifier Tests
# ---------------------------------------------------------------------------

class TestDocumentClassifier:
    def test_gst_certificate_classification(self):
        result = classify_document("GSTIN_Registration_Certificate_2026.pdf")
        assert result.document_type == "gst_certificate"
        assert result.confidence >= 0.90

    def test_udyam_certificate_classification(self):
        result = classify_document("UDYAM_MSME_Registration_Cert.pdf")
        assert result.document_type == "udyam_certificate"
        assert result.confidence >= 0.90

    def test_ca_certificate_classification(self):
        result = classify_document("CA_Annual_Turnover_Cert.pdf")
        assert result.document_type == "ca_turnover_certificate"
        assert result.confidence >= 0.90

    def test_pan_card_classification(self):
        result = classify_document("Company_PAN_Card_Copy.png")
        assert result.document_type == "pan_card"
        assert result.confidence >= 0.90

    def test_fallback_classification(self):
        result = classify_document("unlabeled_document_scan.pdf")
        assert result.document_type == "supporting_document"
        assert result.confidence == 0.50


# ---------------------------------------------------------------------------
# 4. Image Preprocessor Tests
# ---------------------------------------------------------------------------

class TestImagePreprocessor:
    def test_image_preprocessing_pipeline(self):
        """Image is decoded, processed (deskewed/scaled/contrast), and returned as clean bytes."""
        img_bytes = _create_sample_image(width=800, height=1000)
        preprocessed = preprocess_image(img_bytes, target_format="PNG")

        assert preprocessed.width == 800
        assert preprocessed.height == 1000
        assert preprocessed.format == "PNG"
        assert len(preprocessed.image_bytes) > 0


# ---------------------------------------------------------------------------
# 5. Ingestion Pipeline & Acceptance Criteria Tests
# ---------------------------------------------------------------------------

class TestIngestionPipeline:
    def test_invalid_file_type_rejected_before_processing(self):
        """Acceptance Criteria: Invalid file types (.exe, .docx, etc.) are rejected before processing."""
        event_data = {
            "eventId": "evt-001",
            "eventType": "document.uploaded",
            "timestamp": "2026-08-31T04:00:00Z",
            "payload": {
                "tenderId": "t-100",
                "bidderId": "b-100",
                "jobId": "job-100",
                "document": {
                    "fileName": "malicious_script.exe",
                    "fileSize": 1024,
                    "fileType": "exe",
                    "storagePath": "documents/t-100/malicious_script.exe",
                },
            },
        }

        with pytest.raises(IngestionError) as exc_info:
            process_document_uploaded_event(
                event_data=event_data,
                file_bytes=b"MZ fake executable binary content",
            )

        assert "unsupported file type" in str(exc_info.value).lower()

    def test_pdf_ingestion_links_tender_bidder_context_and_emits_event(self):
        """Acceptance Criteria: Processed PDF links tender/bidder context and emits document.preprocessed."""
        pdf_bytes = _create_sample_pdf(num_pages=2, width=595, height=842)
        event_data = {
            "eventId": "evt-002",
            "eventType": "document.uploaded",
            "timestamp": "2026-08-31T04:00:00Z",
            "payload": {
                "tenderId": "tender-alpha",
                "bidderId": "bidder-bravo",
                "jobId": "job-200",
                "document": {
                    "id": "doc-555",
                    "fileName": "GST_Registration_Certificate.pdf",
                    "fileSize": len(pdf_bytes),
                    "fileType": "pdf",
                    "storagePath": "documents/tender-alpha/GST_Registration_Certificate.pdf",
                },
            },
        }

        events = process_document_uploaded_event(
            event_data=event_data,
            file_bytes=pdf_bytes,
        )

        assert len(events) == 1
        emitted = events[0]
        assert emitted["eventType"] == "document.preprocessed"
        assert emitted["payload"]["tenderId"] == "tender-alpha"
        assert emitted["payload"]["bidderId"] == "bidder-bravo"
        assert emitted["payload"]["documentId"] == "doc-555"
        assert emitted["payload"]["jobId"] == "job-200"

        pages = emitted["payload"]["pages"]
        assert len(pages) == 2
        assert pages[0]["pageNumber"] == 1
        assert pages[0]["pageWidth"] == 595
        assert pages[0]["pageHeight"] == 842
        assert pages[1]["pageNumber"] == 2

    def test_zip_ingestion_extracts_and_processes_each_document(self):
        """Acceptance Criteria: ZIP archive extracts documents and emits an event per document."""
        pdf_bytes = _create_sample_pdf(1)
        img_bytes = _create_sample_image()
        zip_data = _create_sample_zip({
            "bid/gst_cert.pdf": pdf_bytes,
            "bid/pan_card.png": img_bytes,
        })

        event_data = {
            "eventId": "evt-003",
            "eventType": "document.uploaded",
            "timestamp": "2026-08-31T04:00:00Z",
            "payload": {
                "tenderId": "tender-gamma",
                "bidderId": "bidder-delta",
                "jobId": "job-300",
                "document": {
                    "id": "doc-zip-001",
                    "fileName": "bid_package.zip",
                    "fileSize": len(zip_data),
                    "fileType": "zip",
                    "storagePath": "documents/tender-gamma/bid_package.zip",
                },
            },
        }

        events = process_document_uploaded_event(
            event_data=event_data,
            file_bytes=zip_data,
        )

        assert len(events) == 2
        for ev in events:
            assert ev["eventType"] == "document.preprocessed"
            assert ev["payload"]["tenderId"] == "tender-gamma"
            assert ev["payload"]["bidderId"] == "bidder-delta"
            assert len(ev["payload"]["pages"]) >= 1
