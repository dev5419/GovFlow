from typing import List, Dict, Any
from collections import defaultdict
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel
from src.compliance_engine.rules.rule_registry import RuleRegistry

CONFIDENCE_THRESHOLD = 0.8

@RuleRegistry.register("gstin_match")
def evaluate_gstin_match(
    fields: List[ExtractedField], 
    tender_id: str, 
    bidder_id: str, 
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Compares GSTIN fields across documents.
    Flags mismatches. Routes low-confidence extractions to NEEDS_REVIEW.
    """
    gstin_fields = [f for f in fields if f.fieldName == "GSTIN" and f.normalizedValue]
    
    if not gstin_fields:
        return []

    flags = []
    
    # Group by value
    value_map = defaultdict(list)
    for field in gstin_fields:
        if field.confidence is not None and field.confidence < CONFIDENCE_THRESHOLD:
            flags.append({
                "status": ComplianceFlagStatus.NEEDS_REVIEW,
                "severity": SeverityLevel.MEDIUM,
                "title": "Low Confidence GSTIN",
                "reason": f"GSTIN extracted from document {field.documentId} has low confidence ({field.confidence}). Manual review required.",
                "evidenceIds": [field.id],
                "aiRecommendation": "Verify GSTIN value against the original document."
            })
            continue
            
        value_map[field.normalizedValue.strip().upper()].append(field)

    if len(value_map) > 1:
        # We have conflicting high-confidence GSTINs
        unique_values = list(value_map.keys())
        evidence_ids = []
        doc_ids = []
        for val, f_list in value_map.items():
            for f in f_list:
                evidence_ids.append(f.id)
                if f.documentId not in doc_ids:
                    doc_ids.append(f.documentId)
        
        doc_ref = " and ".join(doc_ids[:2]) # Just an example if there are many
        if len(doc_ids) > 2:
            doc_ref = f"{doc_ids[0]}, {doc_ids[1]}, and others"
            
        flags.append({
            "status": ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE,
            "severity": SeverityLevel.CRITICAL,
            "title": "GSTIN Mismatch",
            "reason": f"GSTIN mismatch between documents ({doc_ref})",
            "evidenceIds": evidence_ids,
            "aiRecommendation": "Review the conflicting GSTIN values. Bidder may have submitted documents belonging to different entities."
        })
    elif len(value_map) == 1 and len(gstin_fields) > 1:
        # All high confidence and they match
        evidence_ids = [f.id for f in gstin_fields]
        flags.append({
            "status": ComplianceFlagStatus.VERIFIED,
            "severity": SeverityLevel.LOW,
            "title": "GSTIN Match Verified",
            "reason": "GSTIN matches across all submitted documents.",
            "evidenceIds": evidence_ids,
            "aiRecommendation": "No action required."
        })

    return flags
