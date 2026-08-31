import pytest
from src.ocr.extraction_pipeline import ExtractionPipeline
import govflow_shared_types as shared_types

@pytest.fixture
def extraction_pipeline():
    return ExtractionPipeline()

def test_ocr_pipeline_returns_valid_extracted_fields(extraction_pipeline):
    """
    Simulates consuming a preprocessed document page and processing it 
    through PaddleOCR and LayoutLMv3 stubs. 
    Verifies that the returned data exactly matches the ExtractedField contract.
    """
    # 1. Provide mock inputs
    document_id = "doc-123"
    page_number = 1
    page_width = 800.0
    page_height = 1000.0
    image_path = "/mock/storage/path/page1.jpg"

    # 2. Run the pipeline
    extracted_fields = extraction_pipeline.process_page(
        document_id=document_id,
        page_number=page_number,
        page_width=page_width,
        page_height=page_height,
        image_path=image_path
    )

    # 3. Assertions
    assert len(extracted_fields) > 0, "Expected pipeline to extract some fields"
    
    for field in extracted_fields:
        # Validate that it is indeed the Pydantic type
        assert isinstance(field, shared_types.ExtractedField)
        
        # Verify specific normalization rules
        assert field.field_name in ["GSTIN", "Legal Entity Name", "Turnover Value"]
        
        # Verify the BoundingBox contract
        bbox = field.bounding_box
        assert isinstance(bbox, shared_types.BoundingBox)
        assert bbox.page_number == page_number
        assert bbox.page_width == page_width
        assert bbox.page_height == page_height
        assert bbox.x1 < bbox.x2
        assert bbox.y1 < bbox.y2

def test_coordinate_mapper_logic():
    from src.ocr.coordinate_mapper import CoordinateMapper
    
    native_bbox = [[100, 150], [300, 150], [300, 200], [100, 200]]
    mapped = CoordinateMapper.map_to_bounding_box(1, 1000, 1000, native_bbox)
    
    assert mapped.x1 == 100
    assert mapped.y1 == 150
    assert mapped.x2 == 300
    assert mapped.y2 == 200
