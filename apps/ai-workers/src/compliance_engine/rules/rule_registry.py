from typing import Callable, Dict, Any, List
from govflow_shared_types import ExtractedField, Document, RequiredDocument

# Define a standard interface for rules
# Rules receive context (like extracted fields, documents, tender rules)
# and yield a list of flag parameter dictionaries.
RuleFunction = Callable[..., List[Dict[str, Any]]]

class RuleRegistry:
    """Registry to hold and dispatch compliance rules by code."""
    _rules: Dict[str, RuleFunction] = {}

    @classmethod
    def register(cls, rule_code: str) -> Callable[[RuleFunction], RuleFunction]:
        """Decorator to register a rule function."""
        def decorator(func: RuleFunction) -> RuleFunction:
            cls._rules[rule_code] = func
            return func
        return decorator

    @classmethod
    def get_rule(cls, rule_code: str) -> RuleFunction:
        """Retrieves a rule by its code."""
        if rule_code not in cls._rules:
            raise ValueError(f"Rule {rule_code} not found in registry.")
        return cls._rules[rule_code]
        
    @classmethod
    def get_all_rules(cls) -> Dict[str, RuleFunction]:
        """Returns all registered rules."""
        return cls._rules

    @classmethod
    def clear(cls):
        """Clears all rules (useful for testing)."""
        cls._rules.clear()
