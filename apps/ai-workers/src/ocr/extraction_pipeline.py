import uuid
from datetime import datetime, timezone
from typing import List

import govflow_shared_types as shared_types
from src.ocr.paddle_ocr_service import PaddleOCRService
from src.ocr.layoutlmv3_service import LayoutLMv3Service
from src.ocr.field_normalizer import FieldNormalizer
from src.ocr.coordinate_mapper import CoordinateMapper

class ExtractionPipeline:
    """
    Orchestrates OCR -> Layout Classification -> Normalization -> Coordinate Mapping.
    Returns shared_types.ExtractedField records.
    """
    def __init__(self):
        self.ocr_service = PaddleOCRService()
        self.layout_service = LayoutLMv3Service()
        self.normalizer = FieldNormalizer()
        self.coordinate_mapper = CoordinateMapper()

    def process_page(
        self,
        document_id: str,
        page_number: int,
        page_width: float,
        page_height: float,
        image_path: str
    ) -> List[shared_types.ExtractedField]:
        """
        Executes the extraction pipeline for a single document page.
        """
        # 1. OCR Extraction
        ocr_results = self.ocr_service.extract_text(image_path)

        # 2. Layout-Aware Classification
        classified_fields = self.layout_service.classify_fields(image_path, ocr_results)

        extracted_fields = []
        for field in classified_fields:
            # 3. Field Normalization
            canonical_name = self.normalizer.normalize(field["label"])
            
            if not canonical_name:
                continue # Skip fields we don't care about

            # 4. Coordinate Mapping
            bounding_box = self.coordinate_mapper.map_to_bounding_box(
                page_number=page_number,
                page_width=page_width,
                page_height=page_height,
                native_bbox=field["bbox"]
            )

            # Create the shared types ExtractedField contract
            extracted_field = shared_types.ExtractedField(
                id=str(uuid.uuid4()),
                documentId=document_id,
                pageNumber=page_number,
                fieldName=canonical_name,
                rawText=field["value"],
                normalizedValue=field["value"], # MVP: no complex type casting
                confidence=field["confidence"],
                boundingBox=bounding_box,
                extractionMethod="PaddleOCR+LayoutLMv3",
                createdAt=datetime.now(timezone.utc).isoformat()
            )
            extracted_fields.append(extracted_field)

        return extracted_fields
