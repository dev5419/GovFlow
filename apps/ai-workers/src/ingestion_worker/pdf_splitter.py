"""
GovFlow PDF Multipage Splitter
Splits multipage PDFs into per-page records, preserving page order and dimensions.
Extracts pageWidth and pageHeight matching the BoundingBox contract (PRD §12.3).
"""

import io
import os
from dataclasses import dataclass
from typing import List, Optional
from pypdf import PdfReader, PdfWriter


class PdfSplitError(Exception):
    """Raised when PDF splitting or reading fails."""
    pass


@dataclass
class SplitPage:
    """Represents an individual split page from a document."""
    page_number: int        # 1-indexed page number
    page_width: int         # Page width in points / pixels
    page_height: int        # Page height in points / pixels
    page_bytes: bytes       # Single-page PDF binary stream
    media_box: List[float]  # [x0, y0, x1, y1] original bounding coordinates


def split_pdf(pdf_source: bytes | io.BytesIO | str) -> List[SplitPage]:
    """
    Split a multipage PDF into individual 1-page PDF records.
    Extracts page dimensions (width, height) preserving 1-indexed order.
    """
    try:
        if isinstance(pdf_source, bytes):
            reader = PdfReader(io.BytesIO(pdf_source))
        elif isinstance(pdf_source, io.BytesIO):
            reader = PdfReader(pdf_source)
        elif isinstance(pdf_source, str):
            if not os.path.isfile(pdf_source):
                raise PdfSplitError(f"PDF file not found: {pdf_source}")
            reader = PdfReader(pdf_source)
        else:
            raise PdfSplitError("Invalid pdf_source; expected bytes, BytesIO, or file path.")

        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise PdfSplitError("Encrypted / password-protected PDF files cannot be processed.")

        total_pages = len(reader.pages)
        if total_pages == 0:
            raise PdfSplitError("PDF contains 0 pages.")

        split_pages: List[SplitPage] = []

        for idx, page in enumerate(reader.pages):
            page_number = idx + 1  # 1-indexed

            # Extract page dimensions from mediabox
            mediabox = page.mediabox
            width = int(round(float(mediabox.width)))
            height = int(round(float(mediabox.height)))

            # Handle rotation if present in PDF metadata
            rotation = page.get("/Rotate", 0)
            if rotation in (90, 270):
                width, height = height, width

            # Write single-page PDF
            writer = PdfWriter()
            writer.add_page(page)
            out_stream = io.BytesIO()
            writer.write(out_stream)
            page_bytes = out_stream.getvalue()

            split_pages.append(
                SplitPage(
                    page_number=page_number,
                    page_width=width,
                    page_height=height,
                    page_bytes=page_bytes,
                    media_box=[
                        float(mediabox.left),
                        float(mediabox.bottom),
                        float(mediabox.right),
                        float(mediabox.top),
                    ],
                )
            )

        return split_pages

    except PdfSplitError:
        raise
    except Exception as e:
        raise PdfSplitError(f"Failed to split PDF: {e}") from e
