from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.session import SessionLocal

class ReportDataBuilder:
    @staticmethod
    def build_report_data(tender_id: str, bidder_id: str) -> dict:
        """
        Assembles the data payload for the compliance report.
        Ensures strict separation between AI recommendations and Officer Decisions.
        """
        with SessionLocal() as db:
            # 1. Fetch Bidder Info
            bidder_query = text("SELECT id, tender_id, legal_name FROM bidders WHERE id = :bidder_id")
            bidder_row = db.execute(bidder_query, {"bidder_id": bidder_id}).fetchone()
            if not bidder_row:
                raise ValueError(f"Bidder {bidder_id} not found")

            # 2. Fetch Compliance Flags
            flags_query = text("""
                SELECT id, rule_id, status, severity, title, reason, ai_recommendation, anchors
                FROM compliance_flags
                WHERE bidder_id = :bidder_id
                ORDER BY created_at ASC
            """)
            flags_rows = db.execute(flags_query, {"bidder_id": bidder_id}).fetchall()

            report_data = {
                "tender_id": tender_id,
                "bidder_id": bidder_id,
                "legal_name": bidder_row.legal_name,
                "flags": []
            }

            for row in flags_rows:
                # 3. Fetch latest Officer Decision for this flag (if any)
                decision_query = text("""
                    SELECT status, reason_notes, created_at, user_id
                    FROM officer_decisions
                    WHERE flag_id = :flag_id
                    ORDER BY created_at DESC
                    LIMIT 1
                """)
                decision_row = db.execute(decision_query, {"flag_id": row.id}).fetchone()

                # Build flag payload
                flag_data = {
                    "id": row.id,
                    "title": row.title,
                    "rule": row.rule_id,
                    "ai_recommendation": {
                        "status": row.status, # The original AI status
                        "reason": row.reason,
                        "confidence_notes": row.ai_recommendation
                    },
                    "officer_decision": None,
                    "evidence": row.anchors # list of EvidenceAnchor dicts
                }

                if decision_row:
                    flag_data["officer_decision"] = {
                        "status": decision_row.status,
                        "notes": decision_row.reason_notes,
                        "officer_id": decision_row.user_id,
                        "timestamp": decision_row.created_at.isoformat() if decision_row.created_at else None
                    }
                
                report_data["flags"].append(flag_data)

            return report_data
