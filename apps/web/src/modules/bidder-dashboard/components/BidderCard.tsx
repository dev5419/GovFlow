"use client";

import React from "react";
import Link from "next/link";
import type { BidderComplianceSummary } from "@govflow/shared-types";
import {
  FileText,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  ShieldAlert,
  FileQuestion,
  Clock,
} from "lucide-react";

export interface BidderCardProps {
  bidder: BidderComplianceSummary;
  tenderId: string;
}

/**
 * Returns badge styling and icon according to PRD §8.5 node color semantics.
 * Green = Verified / Compliant
 * Amber = Needs Review / Insufficient Evidence
 * Red = Potential Non-Compliance / Confirmed Non-Compliance
 * Grey = Missing Documents
 * Blue = Processing
 */
function getStatusBadgeConfig(status: string) {
  const s = (status || "").toLowerCase();

  if (s.includes("compliant") && !s.includes("non")) {
    return {
      label: "Compliant",
      color: "var(--color-status-verified, #138808)",
      bgColor: "var(--color-status-verified-bg, #E8F5E9)",
      borderColor: "#C8E6C9",
      Icon: CheckCircle2,
    };
  }

  if (s.includes("review") || s.includes("evidence")) {
    return {
      label: "Needs Review",
      color: "var(--color-status-needs-review, #D97706)",
      bgColor: "var(--color-status-needs-review-bg, #FEF3C7)",
      borderColor: "#FDE68A",
      Icon: AlertTriangle,
    };
  }

  if (s.includes("non-compliant") || s.includes("non_compliant")) {
    return {
      label: "Non-Compliant",
      color: "var(--color-status-non-compliant, #DC2626)",
      bgColor: "var(--color-status-non-compliant-bg, #FEE2E2)",
      borderColor: "#FECACA",
      Icon: AlertCircle,
    };
  }

  if (s.includes("missing")) {
    return {
      label: "Missing Documents",
      color: "var(--color-status-missing, #6B7280)",
      bgColor: "var(--color-status-missing-bg, #F3F4F6)",
      borderColor: "#E5E7EB",
      Icon: FileQuestion,
    };
  }

  return {
    label: "Processing",
    color: "var(--color-status-processing, #2563EB)",
    bgColor: "var(--color-status-processing-bg, #EFF6FF)",
    borderColor: "#BFDBFE",
    Icon: Clock,
  };
}

/**
 * Get score color indicator based on compliance score threshold.
 */
function getScoreColor(score: number): string {
  if (score >= 80) return "var(--color-status-verified, #138808)";
  if (score >= 50) return "var(--color-status-needs-review, #D97706)";
  return "var(--color-status-non-compliant, #DC2626)";
}

export function BidderCard({ bidder, tenderId }: BidderCardProps) {
  const badge = getStatusBadgeConfig(bidder.overallStatus);
  const StatusIcon = badge.Icon;
  const scoreColor = getScoreColor(bidder.complianceScore);

  const graphUrl = `/tenders/${encodeURIComponent(
    tenderId
  )}/bidders/${encodeURIComponent(bidder.bidderId)}/graph`;

  const reportUrl = `/tenders/${encodeURIComponent(
    tenderId
  )}/bidders/${encodeURIComponent(bidder.bidderId)}/report`;

  return (
    <article
      className="gov-card flex flex-col justify-between transition-shadow"
      style={{
        backgroundColor: "var(--color-surface, #FFFFFF)",
        border: "1px solid var(--color-border, #DDE2E5)",
        borderRadius: "4px",
        padding: "16px 20px",
      }}
      aria-labelledby={`bidder-title-${bidder.bidderId}`}
    >
      <div>
        {/* Top Header: Bidder Name and Status Badge */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <h3
              id={`bidder-title-${bidder.bidderId}`}
              className="truncate"
              style={{
                fontSize: "16px",
                fontWeight: 700,
                color: "var(--color-primary, #0C2340)",
                margin: 0,
              }}
              title={bidder.bidderName}
            >
              {bidder.bidderName}
            </h3>
            <span
              style={{
                fontSize: "12px",
                color: "var(--color-text-secondary, #595959)",
              }}
            >
              ID: {bidder.bidderId}
            </span>
          </div>

          {/* Status Badge per PRD §8.5 */}
          <div
            className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold whitespace-nowrap"
            style={{
              backgroundColor: badge.bgColor,
              color: badge.color,
              border: `1px solid ${badge.borderColor}`,
              borderRadius: "4px",
            }}
          >
            <StatusIcon size={13} aria-hidden="true" />
            <span>{badge.label}</span>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 p-3 mb-3 bg-[#F8F9FA] rounded border border-[#DDE2E5]">
          {/* Compliance Score */}
          <div>
            <div className="text-[11px] font-semibold text-[#595959] uppercase tracking-wider">
              Compliance
            </div>
            <div
              className="text-lg font-bold"
              style={{ color: scoreColor }}
            >
              {Math.round(bidder.complianceScore)}%
            </div>
          </div>

          {/* Document Count */}
          <div>
            <div className="text-[11px] font-semibold text-[#595959] uppercase tracking-wider">
              Documents
            </div>
            <div className="text-lg font-bold text-[#212529]">
              {bidder.submittedDocuments} / {bidder.totalDocuments}
            </div>
          </div>

          {/* Missing Documents */}
          <div>
            <div className="text-[11px] font-semibold text-[#595959] uppercase tracking-wider">
              Missing Docs
            </div>
            <div
              className="text-lg font-bold"
              style={{
                color:
                  bidder.missingDocuments > 0
                    ? "var(--color-status-non-compliant, #DC2626)"
                    : "#212529",
              }}
            >
              {bidder.missingDocuments}
            </div>
          </div>

          {/* Flag Findings Count */}
          <div>
            <div className="text-[11px] font-semibold text-[#595959] uppercase tracking-wider">
              Flags (Conf / Unres)
            </div>
            <div className="text-lg font-bold text-[#212529]">
              {bidder.confirmedFlagsCount} / {bidder.unresolvedFlagsCount}
            </div>
          </div>
        </div>

        {/* Primary Risk Reasons */}
        <div className="mb-4">
          <div className="text-xs font-bold text-[#0C2340] mb-1.5 flex items-center gap-1.5">
            <ShieldAlert size={14} className="text-[#595959]" aria-hidden="true" />
            <span>Primary Findings & Risk Reasons:</span>
          </div>

          {bidder.primaryRiskReasons && bidder.primaryRiskReasons.length > 0 ? (
            <ul className="list-disc list-inside space-y-1 text-xs text-[#212529] pl-1">
              {bidder.primaryRiskReasons.map((reason, idx) => (
                <li key={idx} className="leading-snug">
                  {reason}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-[#595959] italic pl-1 m-0">
              No active non-compliance risks or flag contradictions reported.
            </p>
          )}
        </div>
      </div>

      {/* Action Buttons Row */}
      <div className="flex items-center justify-between gap-3 pt-3 border-t border-[#DDE2E5]">
        <Link
          href={reportUrl}
          className="gov-btn-secondary text-xs flex-1"
          style={{
            height: "36px",
            fontSize: "13px",
          }}
        >
          <FileText size={14} aria-hidden="true" />
          <span>View Report</span>
        </Link>

        <Link
          href={graphUrl}
          className="gov-btn-primary text-xs flex-1"
          style={{
            height: "36px",
            fontSize: "13px",
          }}
        >
          <span>Open Graph</span>
          <ArrowRight size={14} aria-hidden="true" />
        </Link>
      </div>
    </article>
  );
}
