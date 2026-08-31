import re
from typing import List, Dict, Any
from govflow_shared_types import ExtractedField, ComplianceFlagStatus, SeverityLevel, TenderRule
from src.compliance_engine.rules.rule_registry import RuleRegistry

CONFIDENCE_THRESHOLD = 0.8

def extract_numeric_value(val_str: str) -> float:
    """Extracts the first numeric value from a string. Removes commas."""
    if not val_str:
        return 0.0
    val_str = val_str.replace(',', '')
    match = re.search(r'\d+(\.\d+)?', val_str)
    if match:
        return float(match.group())
    return 0.0

@RuleRegistry.register("turnover_threshold")
def evaluate_turnover_threshold(
    fields: List[ExtractedField], 
    tender_id: str, 
    bidder_id: str, 
    tender_rules: List[TenderRule] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Validates Turnover Value against configured TenderRule threshold.
    """
    flags = []
    
    if not tender_rules:
        return flags
        
    # Find the applicable turnover rule
    turnover_rule = next((r for r in tender_rules if r.ruleType == "turnover_threshold"), None)
    if not turnover_rule or not turnover_rule.parameters or "min_turnover" not in turnover_rule.parameters:
        return flags
        
    min_turnover = float(turnover_rule.parameters["min_turnover"])
    
    turnover_fields = [f for f in fields if f.fieldName == "Turnover Value" and f.normalizedValue]
    
    if not turnover_fields:
        return flags

    for field in turnover_fields:
        if field.confidence is not None and field.confidence < CONFIDENCE_THRESHOLD:
            flags.append({
                "status": ComplianceFlagStatus.NEEDS_REVIEW,
                "severity": SeverityLevel.HIGH,
                "title": "Low Confidence Turnover",
                "reason": f"Turnover extracted from document {field.documentId} has low confidence ({field.confidence}).",
                "evidenceIds": [field.id],
                "aiRecommendation": "Verify the turnover value manually."
            })
            continue
            
        turnover_val = extract_numeric_value(field.normalizedValue)
        
        if turnover_val == 0.0:
            flags.append({
                "status": ComplianceFlagStatus.NEEDS_REVIEW,
                "severity": SeverityLevel.MEDIUM,
                "title": "Unreadable Turnover Value",
                "reason": f"Could not parse a numeric turnover value from '{field.normalizedValue}'.",
                "evidenceIds": [field.id],
                "aiRecommendation": "Verify the value manually."
            })
            continue
            
        if turnover_val < min_turnover:
            flags.append({
                "status": ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE,
                "severity": SeverityLevel.CRITICAL,
                "title": "Turnover Threshold Not Met",
                "reason": f"Declared turnover ({turnover_val}) is below the required minimum ({min_turnover}).",
                "evidenceIds": [field.id],
                "aiRecommendation": "Bidder does not meet the minimum financial turnover requirements."
            })
        else:
            flags.append({
                "status": ComplianceFlagStatus.VERIFIED,
                "severity": SeverityLevel.LOW,
                "title": "Turnover Requirement Met",
                "reason": f"Declared turnover ({turnover_val}) meets or exceeds the required minimum ({min_turnover}).",
                "evidenceIds": [field.id],
                "aiRecommendation": "No action required."
            })

    return flags
