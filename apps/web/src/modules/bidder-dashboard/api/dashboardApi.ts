/**
 * GovFlow Dashboard API Client
 * Calls the API Gateway endpoint for pre-aggregated Bidder Compliance Summaries (F-01).
 * Imports types from @govflow/shared-types — never redefines shapes locally.
 */

import type { BidderComplianceSummary } from "@govflow/shared-types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface GetBidderSummariesParams {
  tenderId: string;
  status?: string;
  sortBy?: "compliance_risk" | "missing_documents" | "processing_status";
  sortOrder?: "asc" | "desc";
}

/**
 * Fetch pre-aggregated bidder compliance summaries for a tender.
 */
export async function getBidderSummaries(
  params: GetBidderSummariesParams
): Promise<BidderComplianceSummary[]> {
  const { tenderId, status, sortBy, sortOrder } = params;

  if (!tenderId) {
    throw new Error("tenderId is required to fetch bidder summaries");
  }

  const query = new URLSearchParams();
  if (status && status !== "all") {
    query.set("status", status);
  }
  if (sortBy) {
    query.set("sort_by", sortBy);
  }
  if (sortOrder) {
    query.set("sort_order", sortOrder);
  }

  const queryString = query.toString();
  const endpoint = `${API_BASE_URL}/tenders/${encodeURIComponent(
    tenderId
  )}/bidders/summaries${queryString ? `?${queryString}` : ""}`;

  const response = await fetch(endpoint, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(
      `Failed to fetch bidder summaries (${response.status} ${response.statusText}): ${errorText}`
    );
  }

  return response.json();
}
