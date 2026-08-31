from typing import List, Dict, Any
from govflow_shared_types import Document, RequiredDocument, ComplianceFlagStatus, SeverityLevel
from src.compliance_engine.rules.rule_registry import RuleRegistry

@RuleRegistry.register("required_document_check")
def evaluate_required_documents(
    documents: List[Document], 
    tender_id: str, 
    bidder_id: str, 
    required_documents: List[RequiredDocument] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Checks if all RequiredDocuments for the tender have a corresponding uploaded Document.
    """
    flags = []
    
    if not required_documents:
        return flags

    # Map uploaded document types
    uploaded_types = {doc.documentType for doc in documents if doc.documentType}

    for req_doc in required_documents:
        if req_doc.documentType not in uploaded_types:
            flags.append({
                "status": ComplianceFlagStatus.MISSING,
                "severity": SeverityLevel.CRITICAL,
                "title": "Missing Required Document",
                "reason": f"Required document type '{req_doc.documentType}' was not found in the submitted package.",
                "evidenceIds": [], # No evidence because it's missing
                "aiRecommendation": f"Bidder failed to provide the mandatory {req_doc.documentType}. Recommend requesting the document or rejecting the bid."
            })
        else:
            # We can optionally emit a VERIFIED flag, but typical compliance engines 
            # only emit VERIFIED flags for content checks rather than mere presence, 
            # or they emit it to turn the graph node Green.
            # We will emit VERIFIED for presence.
            # Get the doc ID(s)
            matched_docs = [doc for doc in documents if doc.documentType == req_doc.documentType]
            flags.append({
                "status": ComplianceFlagStatus.VERIFIED,
                "severity": SeverityLevel.LOW,
                "title": f"{req_doc.documentType} Present",
                "reason": f"Required document type '{req_doc.documentType}' is present.",
                "evidenceIds": [], # Normally we might link the document ID, but evidenceIds are for ExtractedFields. The orchestration layer handles linking to the document.
                "aiRecommendation": "No action required."
            })

    return flags
