import re
from typing import List, Dict, Any
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel
from src.compliance_engine.rules.rule_registry import RuleRegistry

CONFIDENCE_THRESHOLD = 0.8
SIMILARITY_THRESHOLD = 0.7 # We'll use a basic token overlap for now

def normalize_address(address: str) -> str:
    """Normalizes an address string for comparison."""
    if not address:
        return ""
    addr = address.lower()
    addr = re.sub(r'[^\w\s]', '', addr)
    addr = re.sub(r'\s+', ' ', addr).strip()
    return addr

def calculate_similarity(addr1: str, addr2: str) -> float:
    """Calculates a simple token-based Jaccard similarity."""
    tokens1 = set(addr1.split())
    tokens2 = set(addr2.split())
    
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

@RuleRegistry.register("address_match")
def evaluate_address_match(
    fields: List[ExtractedField], 
    tender_id: str, 
    bidder_id: str, 
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Compares Registered Address fields across documents.
    Uses basic token overlap similarity to prevent false positive mismatches.
    """
    address_fields = [f for f in fields if f.fieldName == "Registered Address" and f.normalizedValue]
    
    if not address_fields:
        return []

    flags = []
    
    high_conf_fields = []
    for field in address_fields:
        if field.confidence is not None and field.confidence < CONFIDENCE_THRESHOLD:
            flags.append({
                "status": ComplianceFlagStatus.NEEDS_REVIEW,
                "severity": SeverityLevel.LOW,
                "title": "Low Confidence Address",
                "reason": f"Registered address extracted from document {field.documentId} has low confidence ({field.confidence}). Manual review required.",
                "evidenceIds": [field.id],
                "aiRecommendation": "Verify address value against the original document."
            })
        else:
            high_conf_fields.append(field)

    if len(high_conf_fields) > 1:
        # Compare all pairs (for a small number of docs, O(n^2) is fine)
        mismatch_found = False
        evidence_ids = [f.id for f in high_conf_fields]
        
        base_field = high_conf_fields[0]
        base_norm = normalize_address(base_field.normalizedValue)
        
        for compare_field in high_conf_fields[1:]:
            comp_norm = normalize_address(compare_field.normalizedValue)
            similarity = calculate_similarity(base_norm, comp_norm)
            
            if similarity < SIMILARITY_THRESHOLD:
                mismatch_found = True
                flags.append({
                    "status": ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE,
                    "severity": SeverityLevel.MEDIUM,
                    "title": "Address Mismatch",
                    "reason": f"Registered Address mismatch detected (Similarity: {similarity:.2f}).",
                    "evidenceIds": [base_field.id, compare_field.id],
                    "aiRecommendation": "Review the conflicting addresses to ensure they are the same physical location."
                })
                break # Only flag the first major mismatch to avoid spamming
                
        if not mismatch_found:
            flags.append({
                "status": ComplianceFlagStatus.VERIFIED,
                "severity": SeverityLevel.LOW,
                "title": "Address Match Verified",
                "reason": "Registered Address appears consistent across submitted documents.",
                "evidenceIds": evidence_ids,
                "aiRecommendation": "No action required."
            })

    return flags
