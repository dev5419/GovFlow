from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.compliance_flag import ComplianceFlagModel
import uuid

class ComplianceRepository:
    
    @staticmethod
    async def save_flags(db: AsyncSession, flags: List[Dict[str, Any]]) -> List[ComplianceFlagModel]:
        """
        Persists a batch of compliance flags to the database.
        Enforces immutability by only supporting insert.
        """
        orm_flags = []
        for flag in flags:
            
            # Extract anchors safely, whether they are Pydantic objects or dicts
            anchors_json = []
            for a in flag.get("anchors", []):
                if hasattr(a, "model_dump"):
                    anchors_json.append(a.model_dump())
                else:
                    anchors_json.append(a)
            
            flag_id = flag.get("id") or str(uuid.uuid4())
            
            orm_flag = ComplianceFlagModel(
                id=flag_id,
                tender_id=flag.get("tenderId"),
                bidder_id=flag.get("bidderId"),
                rule_id=flag.get("ruleId"),
                status=flag.get("status"),
                severity=flag.get("severity"),
                title=flag.get("title"),
                reason=flag.get("reason"),
                ai_recommendation=flag.get("aiRecommendation"),
                anchors=anchors_json
            )
            orm_flags.append(orm_flag)
            db.add(orm_flag)
            
        await db.commit()
        return orm_flags
