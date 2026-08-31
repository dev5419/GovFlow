from typing import List, Dict, Any
from govflow_shared_types import ExtractedField, TenderRule, Document, RequiredDocument
from src.compliance_engine.rules.rule_registry import RuleRegistry

class ContradictionDetector:
    """
    Executes applicable rules from RuleRegistry against the bidder's extracted fields.
    Produces raw contradiction candidates (list of flag dicts).
    """

    @staticmethod
    def detect(
        extracted_fields: List[ExtractedField],
        documents: List[Document],
        tender_id: str,
        bidder_id: str,
        tender_rules: List[TenderRule],
        required_documents: List[RequiredDocument],
        resolved_entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        
        raw_flags = []
        all_rules = RuleRegistry.get_all_rules()

        for rule_code, rule_func in all_rules.items():
            flags_from_rule = rule_func(
                fields=extracted_fields,
                documents=documents,
                tender_id=tender_id,
                bidder_id=bidder_id,
                tender_rules=tender_rules,
                required_documents=required_documents,
                resolved_entities=resolved_entities
            )
            
            # Tag each raw flag with the ruleId for traceability (Hard Constraint)
            # We map rule_code back to a ruleId if one exists in tender_rules, 
            # otherwise we fall back to the rule_code as the rule context.
            applicable_tender_rule = next((r for r in tender_rules if r.ruleType == rule_code), None)
            rule_id_to_assign = applicable_tender_rule.id if applicable_tender_rule else f"system-rule-{rule_code}"

            for flag in flags_from_rule:
                flag["ruleId"] = rule_id_to_assign
                raw_flags.append(flag)

        return raw_flags
