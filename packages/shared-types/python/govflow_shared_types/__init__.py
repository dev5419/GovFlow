"""
govflow_shared_types — installable Python package name for shared-types.
Re-exports everything from the sibling __init__.py for clean imports.
"""

# ponytail: the actual models live one level up (packages/shared-types/python/models.py).
# This wrapper package exists solely because Python can't import from a path with hyphens.
import sys
import os

# Add parent dir so we can import from `models.py` next to pyproject.toml
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from models import *  # noqa: F401, F403, E402
from models import (  # noqa: E402
    ComplianceFlagStatus,
    SeverityLevel,
    OfficerDecisionState,
    HighlightColor,
    GraphNodeStatus,
    GraphNodeColor,
    ProcessingJobType,
    ProcessingJobStatus,
    BoundingBox,
    ComplianceFlag,
    OfficerDecision,
    AuditEvent,
    Tender,
    TenderRule,
    RequiredDocument,
    Bidder,
    Document,
    DocumentPage,
    ProcessingJob,
    ExtractedField,
    EvidenceAnchor,
    GraphNodePosition,
    GraphNode,
    GraphEdge,
    BidderComplianceSummary,
)
