from typing import Optional

class FieldNormalizer:
    """
    Normalizes raw extracted field labels into the canonical field set from PRD §8.3.
    """
    def __init__(self):
        # Canonical mappings registry. 
        # Future tender-specific fields can be added here dynamically per PRD §26.
        self.mapping = {
            "gstin": "GSTIN",
            "gst": "GSTIN",
            "udyam": "Udyam Registration Number",
            "udyam registration number": "Udyam Registration Number",
            "legal entity name": "Legal Entity Name",
            "entity name": "Legal Entity Name",
            "name": "Legal Entity Name",
            "registered address": "Registered Address",
            "address": "Registered Address",
            "turnover value": "Turnover Value",
            "turnover": "Turnover Value",
            "financial year": "Financial Year",
            "fy": "Financial Year",
            "certificate date": "Certificate Date",
            "date": "Certificate Date",
            "pan": "PAN",
            "permanent account number": "PAN",
            "authorized signatory": "Authorized Signatory",
            "signatory": "Authorized Signatory",
            "document number": "Document Number",
            "doc no": "Document Number"
        }

    def normalize(self, raw_label: str) -> Optional[str]:
        """
        Normalizes a raw label string to a canonical PRD §8.3 field name.
        Returns None if no canonical mapping is found (so it can be ignored).
        """
        clean_label = raw_label.lower().strip().replace(":", "")
        return self.mapping.get(clean_label)
