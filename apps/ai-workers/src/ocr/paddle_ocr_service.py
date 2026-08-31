from typing import List, Dict, Any

class PaddleOCRService:
    """
    Wraps PaddleOCR for text extraction from page images.
    In a real deployment, this would initialize the PaddleOCR model.
    """
    def __init__(self):
        # TODO: Initialize actual PaddleOCR model here.
        # e.g. self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        pass

    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Stub method for extracting text from an image.
        Returns a list of dictionaries with bounding box and text.
        """
        # TODO: Replace with real model inference: self.ocr.ocr(image_path, cls=True)
        # Mocking an OCR response for a typical certificate
        return [
            {
                "bbox": [[100, 100], [300, 100], [300, 130], [100, 130]],
                "text": "GSTIN: 27ABCDE1234F1Z5",
                "confidence": 0.98
            },
            {
                "bbox": [[100, 150], [400, 150], [400, 180], [100, 180]],
                "text": "Legal Entity Name: ACME CORP",
                "confidence": 0.95
            },
            {
                "bbox": [[100, 200], [250, 200], [250, 230], [100, 230]],
                "text": "Turnover: 5000000",
                "confidence": 0.92
            }
        ]
