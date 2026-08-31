"use client";

import React from "react";
import { ArrowUpDown, RefreshCw, Search } from "lucide-react";

export interface DashboardFiltersProps {
  statusFilter: string;
  onStatusChange: (status: string) => void;
  sortBy?: "compliance_risk" | "missing_documents" | "processing_status";
  onSortByChange: (
    sortBy: "compliance_risk" | "missing_documents" | "processing_status" | undefined
  ) => void;
  sortOrder: "asc" | "desc";
  onSortOrderToggle: () => void;
  searchQuery: string;
  onSearchQueryChange: (query: string) => void;
  onRefresh: () => void;
  isRefetching?: boolean;
}

const FILTER_TABS = [
  { id: "all", label: "All Bidders" },
  { id: "compliant", label: "Compliant" },
  { id: "needs_review", label: "Needs Review" },
  { id: "non_compliant", label: "Non-Compliant" },
  { id: "missing", label: "Missing Documents" },
  { id: "processing", label: "Processing" },
];

export function DashboardFilters({
  statusFilter,
  onStatusChange,
  sortBy,
  onSortByChange,
  sortOrder,
  onSortOrderToggle,
  searchQuery,
  onSearchQueryChange,
  onRefresh,
  isRefetching = false,
}: DashboardFiltersProps) {
  return (
    <div
      className="gov-card mb-6"
      style={{
        backgroundColor: "var(--color-surface, #FFFFFF)",
        border: "1px solid var(--color-border, #DDE2E5)",
        borderRadius: "4px",
        padding: "16px 20px",
      }}
    >
      {/* Top Controls Row */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Status Filter Tabs */}
        <div
          className="flex flex-wrap items-center gap-1.5"
          role="tablist"
          aria-label="Filter bidders by status"
        >
          {FILTER_TABS.map((tab) => {
            const isSelected = statusFilter === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={isSelected}
                onClick={() => onStatusChange(tab.id)}
                className="px-3 py-1.5 text-xs font-semibold rounded transition-colors"
                style={{
                  backgroundColor: isSelected
                    ? "var(--color-primary, #0C2340)"
                    : "var(--color-surface-alt, #F1F4F8)",
                  color: isSelected
                    ? "#FFFFFF"
                    : "var(--color-text-primary, #212529)",
                  border: isSelected
                    ? "1px solid var(--color-primary, #0C2340)"
                    : "1px solid var(--color-border, #DDE2E5)",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Search & Sort Controls */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search Input */}
          <div className="relative flex-1 sm:w-60">
            <Search
              size={14}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#595959]"
              aria-hidden="true"
            />
            <input
              type="text"
              placeholder="Search bidder legal name..."
              value={searchQuery}
              onChange={(e) => onSearchQueryChange(e.target.value)}
              className="gov-input w-full pl-8 pr-3 text-xs"
              aria-label="Search bidder legal name"
              style={{
                height: "36px",
                borderRadius: "4px",
                border: "1px solid #C4CDD5",
                fontSize: "13px",
              }}
            />
          </div>

          {/* Sort Field Selector */}
          <div className="flex items-center gap-1.5">
            <label
              htmlFor="dashboard-sort-by"
              className="text-xs font-semibold text-[#212529] whitespace-nowrap"
            >
              Sort by:
            </label>
            <select
              id="dashboard-sort-by"
              value={sortBy || ""}
              onChange={(e) =>
                onSortByChange(
                  e.target.value
                    ? (e.target.value as
                        | "compliance_risk"
                        | "missing_documents"
                        | "processing_status")
                    : undefined
                )
              }
              className="gov-select text-xs font-medium"
              style={{
                height: "36px",
                borderRadius: "4px",
                border: "1px solid #C4CDD5",
                padding: "4px 8px",
                fontSize: "13px",
              }}
            >
              <option value="">Default (Highest Risk First)</option>
              <option value="compliance_risk">Compliance Risk Score</option>
              <option value="missing_documents">Missing Document Count</option>
              <option value="processing_status">Processing Status</option>
            </select>
          </div>

          {/* Sort Order Toggle */}
          <button
            type="button"
            onClick={onSortOrderToggle}
            className="gov-btn-secondary text-xs"
            title={`Toggle sort order (Current: ${sortOrder.toUpperCase()})`}
            aria-label={`Toggle sort order (Current: ${sortOrder.toUpperCase()})`}
            style={{
              height: "36px",
              padding: "0 10px",
              fontSize: "12px",
              gap: "4px",
            }}
          >
            <ArrowUpDown size={14} aria-hidden="true" />
            <span className="uppercase font-semibold">{sortOrder}</span>
          </button>

          {/* Refresh Button */}
          <button
            type="button"
            onClick={onRefresh}
            disabled={isRefetching}
            className="gov-btn-secondary text-xs"
            title="Refresh Bidder Summaries"
            aria-label="Refresh Bidder Summaries"
            style={{
              height: "36px",
              padding: "0 12px",
              fontSize: "12px",
              gap: "6px",
            }}
          >
            <RefreshCw
              size={14}
              className={isRefetching ? "animate-spin" : ""}
              aria-hidden="true"
            />
            <span>{isRefetching ? "Refreshing..." : "Refresh"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
