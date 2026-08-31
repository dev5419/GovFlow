from typing import List
import govflow_shared_types as shared_types

class CoordinateMapper:
    """
    Maps native OCR coordinates to the BoundingBox contract per PRD §12.3.
    """
    @staticmethod
    def map_to_bounding_box(
        page_number: int,
        page_width: float,
        page_height: float,
        native_bbox: List[List[float]]
    ) -> shared_types.BoundingBox:
        """
        Converts a 4-point polygon bbox [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        or similar from OCR engines to the standard x1, y1, x2, y2 format.
        """
        xs = [point[0] for point in native_bbox]
        ys = [point[1] for point in native_bbox]

        # Extract min and max to get the bounding rectangle
        x1 = min(xs)
        y1 = min(ys)
        x2 = max(xs)
        y2 = max(ys)

        return shared_types.BoundingBox(
            pageNumber=page_number,
            pageWidth=page_width,
            pageHeight=page_height,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )
