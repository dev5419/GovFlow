from typing import List

# Order of priority: 0 is highest, 4 is lowest
STATUS_PRIORITY = {
    "PROCESSING": 0,
    "MISSING": 1,
    "CONFIRMED_NON_COMPLIANCE": 2,
    "POTENTIAL_NON_COMPLIANCE": 2, # Treat these interchangeably for graph priority
    "INSUFFICIENT_EVIDENCE": 3,
    "NEEDS_REVIEW": 3, # Treat these interchangeably for graph priority
    "VERIFIED": 4
}

def resolve_node_status(processing_status: str, compliance_flags: List[str]) -> str:
    """
    Resolves the canonical node status based on the strict PRD 8.5 priority:
    Processing > Missing > Non-Compliance > Needs Review/Insufficient Evidence > Verified.
    
    :param processing_status: "QUEUED", "PROCESSING", "COMPLETED", "FAILED" or "MISSING"
    :param compliance_flags: List of flag statuses e.g. ["VERIFIED", "POTENTIAL_NON_COMPLIANCE"]
    """
    
    # Priority 1: Processing
    # If the document hasn't finished extracting/processing, it supersedes all compliance flags.
    if processing_status in ["QUEUED", "PROCESSING", "FAILED"]:
        return "PROCESSING"

    # Priority 2: Missing
    if processing_status == "MISSING":
        return "MISSING"
        
    # If no flags exist yet (and it's completed processing), we assume verified 
    # until the compliance engine runs, or we can assume it's just VERIFIED.
    # The PRD states that Verified is the base state if nothing is wrong.
    if not compliance_flags:
        return "VERIFIED"

    # Evaluate flags
    best_priority = 99
    best_status = "VERIFIED"
    
    for flag in compliance_flags:
        priority = STATUS_PRIORITY.get(flag, 99)
        if priority < best_priority:
            best_priority = priority
            best_status = flag

    # We map equivalent severities to a single graph status if needed, 
    # but the PRD specifies rendering based on the exact string.
    # The nodeColors.ts maps POTENTIAL_NON_COMPLIANCE and CONFIRMED_NON_COMPLIANCE both to red.
    return best_status
