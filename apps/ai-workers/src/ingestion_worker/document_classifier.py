"""
GovFlow Document First-Pass Classifier
Categorizes incoming tender bid documents into canonical categories per PRD §8.2 and §8.3.
Uses heuristic keyword and filename pattern matching for fast, accurate initial triage.
"""

import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ClassificationResult:
    """Document classification outcome."""
    document_type: str        # Canonical internal key (e.g. gst_certificate)
    display_name: str         # Human-readable title (e.g. GST Registration Certificate)
    confidence: float         # 0.0 to 1.0 confidence
    matched_patterns: List[str]


# Rules configuration: (document_type, display_name, regex_patterns, default_confidence)
_CLASSIFICATION_RULES: List[Tuple[str, str, List[str], float]] = [
    (
        "gst_certificate",
        "GST Registration Certificate",
        [
            r"gst",
            r"gstin",
            r"gst_reg",
            r"form_gst_reg",
            r"goods_and_services_tax",
        ],
        0.95,
    ),
    (
        "udyam_certificate",
        "Udyam / MSME Registration Certificate",
        [
            r"udyam",
            r"msme",
            r"udyam_reg",
            r"small_medium_enterprise",
            r"dic_reg",
        ],
        0.95,
    ),
    (
        "ca_turnover_certificate",
        "CA Turnover & Net Worth Certificate",
        [
            r"ca_cert",
            r"ca_certificate",
            r"turnover_cert",
            r"chartered_accountant",
            r"annual_turnover",
            r"net_worth_cert",
            r"udin",
        ],
        0.90,
    ),
    (
        "financial_statement",
        "Audited Financial Statement / Balance Sheet",
        [
            r"balance_sheet",
            r"profit_and_loss",
            r"pnl",
            r"financial_statement",
            r"audited_accounts",
            r"audit_report",
            r"financial_year",
        ],
        0.88,
    ),
    (
        "pan_card",
        "Permanent Account Number (PAN) Card",
        [
            r"pan_card",
            r"pan_cert",
            r"pan_copy",
            r"nsdl_pan",
            r"uti_pan",
            r"\bpan\b",
        ],
        0.92,
    ),
    (
        "incorporation_certificate",
        "Certificate of Incorporation / MCA Registration",
        [
            r"incorporation",
            r"coi",
            r"mca_reg",
            r"cin_certificate",
            r"roc_reg",
            r"partnership_deed",
            r"llp_agreement",
        ],
        0.90,
    ),
    (
        "bid_security_declaration",
        "Bid Security / EMD Declaration",
        [
            r"emd",
            r"bid_security",
            r"earnest_money",
            r"bank_guarantee",
            r"bg_copy",
        ],
        0.85,
    ),
    (
        "non_blacklisting_declaration",
        "Non-Blacklisting & Integrity Declaration",
        [
            r"non_blacklist",
            r"blacklisting",
            r"debarment",
            r"integrity_pact",
            r"affidavit",
        ],
        0.85,
    ),
    (
        "technical_proposal",
        "Technical Bid / Specifications Document",
        [
            r"technical_bid",
            r"technical_proposal",
            r"specifications",
            r"scope_of_work",
            r"methodology",
        ],
        0.80,
    ),
]


def classify_document(
    file_name: str,
    text_sample: Optional[str] = None,
    declared_type: Optional[str] = None,
) -> ClassificationResult:
    """
    Classify a document using its filename, optional text snippet, and declared metadata.
    """
    if declared_type:
        # If user/API explicitly declared the document type, check against rules
        for doc_type, display_name, _, conf in _CLASSIFICATION_RULES:
            if declared_type.lower() in (doc_type, display_name.lower()):
                return ClassificationResult(
                    document_type=doc_type,
                    display_name=display_name,
                    confidence=conf,
                    matched_patterns=["explicit_declaration"],
                )

    # Normalize filename for matching
    base_name, _ = os.path.splitext(file_name.lower())
    clean_target = re.sub(r"[_\-\.\s]+", "_", base_name)

    # Search against heuristic rules
    for doc_type, display_name, patterns, base_conf in _CLASSIFICATION_RULES:
        matched: List[str] = []
        for pat in patterns:
            if re.search(pat, clean_target, re.IGNORECASE):
                matched.append(f"filename:{pat}")

            if text_sample and re.search(pat, text_sample, re.IGNORECASE):
                matched.append(f"text:{pat}")

        if matched:
            # Boost confidence if multiple patterns or both filename & text matched
            conf = min(1.0, base_conf + (0.03 * (len(matched) - 1)))
            return ClassificationResult(
                document_type=doc_type,
                display_name=display_name,
                confidence=conf,
                matched_patterns=matched,
            )

    # Fallback to general supporting document
    return ClassificationResult(
        document_type="supporting_document",
        display_name="General Supporting Document",
        confidence=0.50,
        matched_patterns=["fallback_default"],
    )
