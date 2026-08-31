from typing import List, Dict, Any
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel

class ConfidenceScorer:
    """
    Combines OCR confidence with rule-match certainty. 
    Acts as a safety net: if a rule returned POTENTIAL_NON_COMPLIANCE but the underlying
    evidence fields have low confidence, it forces a downgrade to NEEDS_REVIEW.
    Satisfies §8.4's confidence-vs-compliance distinction requirement.
    """

    CONFIDENCE_THRESHOLD = 0.8

    @classmethod
    def score_and_adjust(
        cls, 
        raw_flags: List[Dict[str, Any]], 
        extracted_fields: List[ExtractedField]
    ) -> List[Dict[str, Any]]:
        
        field_map = {f.id: f for f in extracted_fields}
        adjusted_flags = []

        for flag in raw_flags:
            if flag["status"] == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE:
                # Check underlying evidence confidence
                evidence_ids = flag.get("evidenceIds", [])
                
                has_low_confidence = False
                for eid in evidence_ids:
                    field = field_map.get(eid)
                    if field and field.confidence is not None and field.confidence < cls.CONFIDENCE_THRESHOLD:
                        has_low_confidence = True
                        break
                
                if has_low_confidence:
                    flag["status"] = ComplianceFlagStatus.NEEDS_REVIEW
                    flag["severity"] = SeverityLevel.MEDIUM
                    flag["title"] = f"[Downgraded] {flag.get('title', 'Potential Issue')}"
                    flag["reason"] = f"{flag.get('reason')} (Downgraded to Needs Review due to low OCR confidence in supporting evidence)."
            
            adjusted_flags.append(flag)

        return adjusted_flags
