"use client";

import React from "react";
import type { BidderComplianceSummary } from "@govflow/shared-types";
import { CheckCircle2, AlertTriangle, XCircle, FileQuestion, Clock } from "lucide-react";

interface RiskSummaryProps {
  bidders: BidderComplianceSummary[];
  activeFilter?: string;
  onFilterSelect?: (status: string) => void;
}

export function RiskSummary({
  bidders,
  activeFilter = "all",
  onFilterSelect,
}: RiskSummaryProps) {
  const totalBidders = bidders.length;

  const counts = bidders.reduce(
    (acc, bidder) => {
      const status = (bidder.overallStatus || "").toLowerCase();
      if (status.includes("compliant") && !status.includes("non")) {
        acc.compliant += 1;
      } else if (status.includes("review") || status.includes("evidence")) {
        acc.needsReview += 1;
      } else if (status.includes("non-compliant") || status.includes("non_compliant")) {
        acc.nonCompliant += 1;
      } else if (status.includes("missing")) {
        acc.missing += 1;
      } else if (status.includes("processing") || status.includes("pending")) {
        acc.processing += 1;
      } else {
        acc.other += 1;
      }
      return acc;
    },
    {
      compliant: 0,
      needsReview: 0,
      nonCompliant: 0,
      missing: 0,
      processing: 0,
      other: 0,
    }
  );

  const buckets = [
    {
      id: "all",
      label: "Total Bidders",
      count: totalBidders,
      color: "#0C2340",
      bgColor: "#F1F4F8",
      borderColor: "#DDE2E5",
      icon: null,
    },
    {
      id: "compliant",
      label: "Verified / Compliant",
      count: counts.compliant,
      color: "#138808",
      bgColor: "#E8F5E9",
      borderColor: "#C8E6C9",
      icon: CheckCircle2,
    },
    {
      id: "needs_review",
      label: "Needs Review",
      count: counts.needsReview,
      color: "#D97706",
      bgColor: "#FEF3C7",
      borderColor: "#FDE68A",
      icon: AlertTriangle,
    },
    {
      id: "non_compliant",
      label: "Non-Compliant",
      count: counts.nonCompliant,
      color: "#DC2626",
      bgColor: "#FEE2E2",
      borderColor: "#FECACA",
      icon: XCircle,
    },
    {
      id: "missing",
      label: "Missing Documents",
      count: counts.missing,
      color: "#6B7280",
      bgColor: "#F3F4F6",
      borderColor: "#E5E7EB",
      icon: FileQuestion,
    },
    {
      id: "processing",
      label: "Processing",
      count: counts.processing,
      color: "#2563EB",
      bgColor: "#EFF6FF",
      borderColor: "#BFDBFE",
      icon: Clock,
    },
  ];

  return (
    <section
      aria-label="Tender Risk Summary"
      className="gov-card mb-6"
      style={{
        backgroundColor: "var(--color-surface, #FFFFFF)",
        border: "1px solid var(--color-border, #DDE2E5)",
        borderRadius: "4px",
        padding: "16px 20px",
      }}
    >
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-3 mb-3 border-b border-[#DDE2E5] gap-2">
        <div>
          <h2
            style={{
              fontSize: "16px",
              fontWeight: 600,
              color: "var(--color-primary, #0C2340)",
              margin: 0,
            }}
          >
            Tender Compliance Overview
          </h2>
          <p
            style={{
              fontSize: "12px",
              color: "var(--color-text-secondary, #595959)",
              margin: 0,
            }}
          >
            Summary of evaluated bidder packages and active findings
          </p>
        </div>
        <div className="text-xs text-[#595959] font-medium">
          {totalBidders} {totalBidders === 1 ? "Bidder" : "Bidders"} Registered
        </div>
      </div>

      {/* Metric Tiles */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {buckets.map((bucket) => {
          const Icon = bucket.icon;
          const isSelected = activeFilter === bucket.id;

          return (
            <button
              key={bucket.id}
              type="button"
              onClick={() => onFilterSelect?.(bucket.id)}
              className="flex flex-col text-left p-3 transition-colors relative"
              style={{
                backgroundColor: bucket.bgColor,
                border: isSelected
                  ? `2px solid ${bucket.color}`
                  : `1px solid ${bucket.borderColor}`,
                borderRadius: "4px",
                cursor: onFilterSelect ? "pointer" : "default",
              }}
              aria-pressed={isSelected}
            >
              <div className="flex items-center justify-between w-full mb-1">
                <span
                  style={{
                    fontSize: "11px",
                    fontWeight: 600,
                    textTransform: "uppercase",
                    letterSpacing: "0.025em",
                    color: bucket.color,
                  }}
                >
                  {bucket.label}
                </span>
                {Icon && (
                  <Icon
                    size={14}
                    style={{ color: bucket.color }}
                    aria-hidden="true"
                  />
                )}
              </div>
              <span
                style={{
                  fontSize: "22px",
                  fontWeight: 700,
                  color: bucket.color,
                  lineHeight: 1.2,
                }}
              >
                {bucket.count}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
