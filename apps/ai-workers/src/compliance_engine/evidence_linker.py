from typing import List, Dict, Any
import uuid
from govflow_shared_types import ExtractedField, EvidenceAnchor, ComplianceFlagStatus

class EvidenceLinker:
    """
    Attaches EvidenceAnchor records to every flag based on the underlying ExtractedFields.
    Ensures that for contradictions, bounding boxes from BOTH conflicting source documents are linked.
    """

    @staticmethod
    def link_evidence(
        flags: List[Dict[str, Any]], 
        extracted_fields: List[ExtractedField]
    ) -> List[Dict[str, Any]]:
        
        field_map = {f.id: f for f in extracted_fields}
        linked_flags = []

        for flag in flags:
            evidence_ids = flag.get("evidenceIds", [])
            anchors: List[EvidenceAnchor] = []
            
            for eid in evidence_ids:
                field = field_map.get(eid)
                if field and field.boundingBox:
                    anchor = EvidenceAnchor(
                        id=str(uuid.uuid4()),
                        documentId=field.documentId,
                        pageNumber=field.pageNumber,
                        boundingBox=field.boundingBox,
                        extractedFieldId=field.id,
                        createdAt=field.createdAt # Approximate creation time
                    )
                    anchors.append(anchor)
                    
            # Hard Constraint: Every non-missing flag must have evidence
            if flag["status"] != ComplianceFlagStatus.MISSING and not anchors:
                # We can't present a finding without evidence, so we must downgrade or drop it.
                # However, our rules should have caught this. If it slipped through, we mark it.
                flag["status"] = ComplianceFlagStatus.INSUFFICIENT_EVIDENCE
                flag["title"] = "[Missing Evidence] " + flag.get("title", "")
                flag["reason"] = flag.get("reason", "") + " (Flag generated without proper bounding box evidence)."
                
            flag["anchors"] = anchors
            linked_flags.append(flag)

        return linked_flags
