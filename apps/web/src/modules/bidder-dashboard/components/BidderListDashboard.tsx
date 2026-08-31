"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { useBidderList } from "../hooks/useBidderList";
import { RiskSummary } from "./RiskSummary";
import { DashboardFilters } from "./DashboardFilters";
import { BidderCard } from "./BidderCard";
import {
  Upload,
  Layers,
  AlertCircle,
  Clock,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";

export interface BidderListDashboardProps {
  tenderId: string;
  tenderTitle?: string;
  tenderNumber?: string;
}

export function BidderListDashboard({
  tenderId,
  tenderTitle = "Procurement Tender",
  tenderNumber,
}: BidderListDashboardProps) {
  const [searchQuery, setSearchQuery] = useState("");

  const {
    data: bidders,
    isLoading,
    isRefetching,
    error,
    statusFilter,
    sortBy,
    sortOrder,
    setStatusFilter,
    setSortBy,
    setSortOrder,
    refetch,
    lastFetchedAt,
  } = useBidderList(tenderId, {
    autoRefreshIntervalMs: 15000, // Background polling for evaluation updates per PRD §8.1
  });

  // Client-side text search by bidder legal name or ID
  const filteredBidders = useMemo(() => {
    if (!searchQuery.trim()) return bidders;
    const query = searchQuery.toLowerCase().trim();
    return bidders.filter(
      (b) =>
        b.bidderName.toLowerCase().includes(query) ||
        b.bidderId.toLowerCase().includes(query)
    );
  }, [bidders, searchQuery]);

  const handleSortOrderToggle = () => {
    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] pb-12">
      {/* Top Government Platform Header Bar per design.md */}
      <header
        className="w-full"
        style={{
          backgroundColor: "var(--color-primary, #0C2340)",
          color: "#FFFFFF",
        }}
      >
        <div className="gov-container py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold bg-[#1B365D] text-[#FFFFFF] border border-[#2A4B7C]">
                TENDER WORKSPACE
              </span>
              {tenderNumber && (
                <span className="text-xs text-[#DDE2E5] font-mono">
                  Ref: {tenderNumber}
                </span>
              )}
            </div>
            <h1
              className="text-xl md:text-2xl font-bold tracking-tight text-white m-0"
              style={{
                fontSize: "var(--font-h1, 24px)",
                color: "#FFFFFF",
              }}
            >
              {tenderTitle}
            </h1>
            <p className="text-xs text-[#DDE2E5] mt-0.5 m-0">
              Active Tender ID:{" "}
              <span className="font-mono font-medium">{tenderId}</span>
            </p>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center gap-3">
            <Link
              href={`/tenders/${encodeURIComponent(tenderId)}/upload`}
              className="gov-btn-primary"
              style={{
                backgroundColor: "var(--color-accent, #F37021)",
                color: "#FFFFFF",
                fontSize: "13px",
                height: "38px",
                padding: "0 16px",
              }}
            >
              <Upload size={15} aria-hidden="true" />
              <span>Batch Upload Bids</span>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Body Container */}
      <main className="gov-container pt-6">
        {/* Navigation Breadcrumb / Context Bar */}
        <nav
          aria-label="Breadcrumb"
          className="flex items-center justify-between text-xs text-[#595959] mb-4 pb-2 border-b border-[#DDE2E5]"
        >
          <div className="flex items-center gap-1.5 font-medium">
            <Link href="/" className="hover:underline text-[#0C2340]">
              Tenders
            </Link>
            <span>/</span>
            <span className="font-semibold text-[#212529]">
              Bidder Compliance Dashboard
            </span>
          </div>

          {lastFetchedAt && (
            <div className="flex items-center gap-1.5 text-[11px] text-[#595959]">
              <Clock size={12} aria-hidden="true" />
              <span>
                Last updated: {lastFetchedAt.toLocaleTimeString()}
              </span>
            </div>
          )}
        </nav>

        {/* Loading State */}
        {isLoading && bidders.length === 0 ? (
          <div
            className="gov-card flex flex-col items-center justify-center p-12 text-center my-8"
            role="status"
            aria-live="polite"
          >
            <RefreshCw
              size={32}
              className="animate-spin text-[#0C2340] mb-3"
              aria-hidden="true"
            />
            <h2 className="text-base font-bold text-[#0C2340] m-0">
              Loading Bidder Compliance Data...
            </h2>
            <p className="text-xs text-[#595959] mt-1 m-0">
              Fetching pre-aggregated compliance scores and flag findings from
              API Gateway
            </p>
          </div>
        ) : error ? (
          /* Error State */
          <div
            className="gov-card p-6 my-8 border-l-4 border-l-[#DC2626]"
            role="alert"
            style={{
              backgroundColor: "#FFF5F5",
              borderColor: "#FECACA",
            }}
          >
            <div className="flex items-start gap-3">
              <AlertCircle
                size={20}
                className="text-[#DC2626] shrink-0 mt-0.5"
                aria-hidden="true"
              />
              <div className="flex-1">
                <h3 className="text-sm font-bold text-[#DC2626] m-0">
                  Unable to load bidder dashboard data
                </h3>
                <p className="text-xs text-[#212529] mt-1 mb-3">
                  {error.message ||
                    "Network error connecting to API Gateway. Please verify API service is running."}
                </p>
                <button
                  type="button"
                  onClick={() => refetch()}
                  className="gov-btn-secondary text-xs"
                  style={{ height: "32px", padding: "0 12px" }}
                >
                  <RefreshCw size={13} aria-hidden="true" />
                  <span>Retry Request</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Main Dashboard Content */
          <>
            {/* 1. Risk Summary Strip */}
            <RiskSummary
              bidders={bidders}
              activeFilter={statusFilter}
              onFilterSelect={(status) => setStatusFilter(status)}
            />

            {/* 2. Dashboard Filter and Sort Bar */}
            <DashboardFilters
              statusFilter={statusFilter}
              onStatusChange={setStatusFilter}
              sortBy={sortBy}
              onSortByChange={setSortBy}
              sortOrder={sortOrder}
              onSortOrderToggle={handleSortOrderToggle}
              searchQuery={searchQuery}
              onSearchQueryChange={setSearchQuery}
              onRefresh={refetch}
              isRefetching={isRefetching}
            />

            {/* 3. Bidder Cards Grid (12-Column Responsive) */}
            {filteredBidders.length === 0 ? (
              <div
                className="gov-card flex flex-col items-center justify-center p-12 text-center"
                style={{
                  backgroundColor: "var(--color-surface, #FFFFFF)",
                  border: "1px solid var(--color-border, #DDE2E5)",
                  borderRadius: "4px",
                }}
              >
                <Layers
                  size={36}
                  className="text-[#595959] mb-3"
                  aria-hidden="true"
                />
                <h3
                  style={{
                    fontSize: "16px",
                    fontWeight: 700,
                    color: "var(--color-primary, #0C2340)",
                    margin: 0,
                  }}
                >
                  No Bidders Found
                </h3>
                <p
                  style={{
                    fontSize: "13px",
                    color: "var(--color-text-secondary, #595959)",
                    marginTop: "4px",
                    marginBottom: "16px",
                    maxWidth: "400px",
                  }}
                >
                  {searchQuery || statusFilter !== "all"
                    ? "No bidder records match the active status filter or search term. Try resetting your filters."
                    : "No bidder packages have been uploaded or processed for this tender yet."}
                </p>
                {(searchQuery || statusFilter !== "all") && (
                  <button
                    type="button"
                    onClick={() => {
                      setStatusFilter("all");
                      setSearchQuery("");
                    }}
                    className="gov-btn-secondary text-xs"
                  >
                    Reset All Filters
                  </button>
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredBidders.map((bidder) => (
                  <BidderCard
                    key={bidder.bidderId}
                    bidder={bidder}
                    tenderId={tenderId}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
