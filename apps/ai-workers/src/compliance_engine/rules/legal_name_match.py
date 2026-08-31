import re
from typing import List, Dict, Any
from collections import defaultdict
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel
from src.compliance_engine.rules.rule_registry import RuleRegistry

CONFIDENCE_THRESHOLD = 0.8

def normalize_legal_name(name: str) -> str:
    """
    Normalizes legal entity names by lowercasing, stripping punctuation, 
    and removing common corporate suffixes.
    """
    if not name:
        return ""
        
    name = name.lower()
    
    # Remove punctuation
    name = re.sub(r'[^\w\s]', '', name)
    
    # Remove common suffixes
    suffixes = [r'\bpvt\b', r'\bltd\b', r'\blimited\b', r'\bprivate\b', r'\bllc\b', r'\binc\b', r'\bco\b', r'\bcorp\b']
    for suffix in suffixes:
        name = re.sub(suffix, '', name)
        
    # Replace multiple spaces with a single space and strip
    name = re.sub(r'\s+', ' ', name).strip()
    return name

@RuleRegistry.register("legal_name_match")
def evaluate_legal_name_match(
    fields: List[ExtractedField], 
    tender_id: str, 
    bidder_id: str, 
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Compares Legal Entity Name fields across documents with normalization.
    """
    name_fields = [f for f in fields if f.fieldName == "Legal Entity Name" and f.normalizedValue]
    
    if not name_fields:
        return []

    flags = []
    value_map = defaultdict(list)
    
    for field in name_fields:
        if field.confidence is not None and field.confidence < CONFIDENCE_THRESHOLD:
            flags.append({
                "status": ComplianceFlagStatus.NEEDS_REVIEW,
                "severity": SeverityLevel.MEDIUM,
                "title": "Low Confidence Legal Name",
                "reason": f"Legal name extracted from document {field.documentId} has low confidence ({field.confidence}). Manual review required.",
                "evidenceIds": [field.id],
                "aiRecommendation": "Verify legal entity name value against the original document."
            })
            continue
            
        norm_val = normalize_legal_name(field.normalizedValue)
        value_map[norm_val].append(field)

    if len(value_map) > 1:
        unique_values = list(value_map.keys())
        evidence_ids = []
        doc_ids = []
        raw_values = []
        for val, f_list in value_map.items():
            for f in f_list:
                evidence_ids.append(f.id)
                if f.documentId not in doc_ids:
                    doc_ids.append(f.documentId)
                if f.normalizedValue not in raw_values:
                    raw_values.append(f.normalizedValue)
        
        doc_ref = " and ".join(doc_ids[:2])
        if len(doc_ids) > 2:
            doc_ref = f"{doc_ids[0]}, {doc_ids[1]}, and others"
            
        flags.append({
            "status": ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE,
            "severity": SeverityLevel.HIGH,
            "title": "Legal Name Mismatch",
            "reason": f"Legal Entity Name mismatch between documents ({doc_ref}). Values found: {', '.join(raw_values)}",
            "evidenceIds": evidence_ids,
            "aiRecommendation": "Review the conflicting legal names. Verify if they refer to the same entity or if different entities are involved."
        })
    elif len(value_map) == 1 and len(name_fields) > 1:
        evidence_ids = [f.id for f in name_fields]
        flags.append({
            "status": ComplianceFlagStatus.VERIFIED,
            "severity": SeverityLevel.LOW,
            "title": "Legal Name Match Verified",
            "reason": "Legal Entity Name matches across submitted documents.",
            "evidenceIds": evidence_ids,
            "aiRecommendation": "No action required."
        })

    return flags
