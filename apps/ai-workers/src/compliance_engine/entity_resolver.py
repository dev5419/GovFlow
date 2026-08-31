from typing import List, Dict, Any
from govflow_shared_types import ExtractedField

class EntityResolver:
    """
    Resolves 'the same real-world entity' across multiple extracted fields.
    For MVP, we gather all fields related to identity to supply to the rules.
    """
    
    @staticmethod
    def resolve(extracted_fields: List[ExtractedField]) -> Dict[str, Any]:
        """
        Groups the extracted fields logically before passing to rules.
        """
        resolved_data = {
            "all_fields": extracted_fields,
            "entity_names": [f for f in extracted_fields if f.fieldName == "Legal Entity Name"],
            "gstins": [f for f in extracted_fields if f.fieldName == "GSTIN"],
            "addresses": [f for f in extracted_fields if f.fieldName == "Registered Address"],
        }
        return resolved_data
