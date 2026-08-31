from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from govflow_shared_types import ExtractedField, Document, RequiredDocument, TenderRule, ComplianceFlagStatus
from src.compliance_engine.entity_resolver import EntityResolver
from src.compliance_engine.contradiction_detector import ContradictionDetector
from src.compliance_engine.confidence_scorer import ConfidenceScorer
from src.compliance_engine.evidence_linker import EvidenceLinker
from src.database.repositories.compliance_repository import ComplianceRepository
from src.database.models.bidder_compliance_summary import BidderComplianceSummaryModel

class ComplianceEngine:
    """
    Orchestrates the compliance evaluation process.
    """
    
    @staticmethod
    async def evaluate(
        db: AsyncSession,
        extracted_fields: List[ExtractedField],
        documents: List[Document],
        tender_rules: List[TenderRule],
        required_documents: List[RequiredDocument],
        tender_id: str,
        bidder_id: str
    ) -> List[Dict[str, Any]]:
        
        # 1. Entity Resolution
        resolved_entities = EntityResolver.resolve(extracted_fields)
        
        # 2. Contradiction Detection
        raw_flags = ContradictionDetector.detect(
            extracted_fields=extracted_fields,
            documents=documents,
            tender_id=tender_id,
            bidder_id=bidder_id,
            tender_rules=tender_rules,
            required_documents=required_documents,
            resolved_entities=resolved_entities
        )
        
        # 3. Confidence Scoring
        scored_flags = ConfidenceScorer.score_and_adjust(
            raw_flags=raw_flags,
            extracted_fields=extracted_fields
        )
        
        # 4. Evidence Linking
        linked_flags = EvidenceLinker.link_evidence(
            flags=scored_flags,
            extracted_fields=extracted_fields
        )
        
        # Ensure tender_id and bidder_id are set on all flags
        for flag in linked_flags:
            flag["tenderId"] = tender_id
            flag["bidderId"] = bidder_id

        # 5. Persist Flags (Immutable append-only insertion)
        await ComplianceRepository.save_flags(db, linked_flags)
        
        # 6. Update Bidder Compliance Summary
        await ComplianceEngine._update_bidder_summary(db, tender_id, bidder_id, linked_flags)
        
        return linked_flags

    @staticmethod
    async def _update_bidder_summary(db: AsyncSession, tender_id: str, bidder_id: str, flags: List[Dict[str, Any]]):
        stmt = select(BidderComplianceSummaryModel).where(
            BidderComplianceSummaryModel.tender_id == tender_id,
            BidderComplianceSummaryModel.bidder_id == bidder_id
        )
        result = await db.execute(stmt)
        summary = result.scalars().first()
        
        if not summary:
            return # Should have been created during ingestion, but safe fallback
            
        # Recalculate metrics
        missing = sum(1 for f in flags if f.get("status") == ComplianceFlagStatus.MISSING)
        unresolved = sum(1 for f in flags if f.get("status") in [
            ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE, 
            ComplianceFlagStatus.NEEDS_REVIEW
        ])
        
        summary.missing_documents = missing
        summary.unresolved_flags = unresolved
        summary.processing_status = "completed"
        
        critical_flags = [f for f in flags if f.get("severity") == "critical" and f.get("status") == ComplianceFlagStatus.POTENTIAL_NON_COMPLIANCE]
        if critical_flags:
            summary.primary_risk_reasons = ", ".join([f.get("title", "") for f in critical_flags[:2]])
            summary.overall_score = 0.0 # Just a simplistic heuristic
            
        db.add(summary)
        await db.commit()
