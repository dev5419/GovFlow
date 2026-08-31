/**
 * Runnable self-check for bidder dashboard API client and query construction.
 * Uses standard assertions (no external test framework required).
 */

import { getBidderSummaries } from "../api/dashboardApi";
import type { BidderComplianceSummary } from "@govflow/shared-types";

export async function runDashboardApiSelfCheck(): Promise<boolean> {
  // Test 1: Throws error when tenderId is empty
  let threwForEmptyTender = false;
  try {
    await getBidderSummaries({ tenderId: "" });
  } catch (err) {
    threwForEmptyTender = true;
  }
  if (!threwForEmptyTender) {
    throw new Error("Expected getBidderSummaries to throw when tenderId is empty");
  }

  // Test 2: Handles mock fetch response and correctly constructs URL
  const mockSummary: BidderComplianceSummary = {
    bidderId: "b-001",
    tenderId: "t-001",
    bidderName: "Acme Infrastructure Ltd",
    complianceScore: 92.5,
    totalDocuments: 6,
    submittedDocuments: 6,
    missingDocuments: 0,
    verifiedFlagsCount: 5,
    needsReviewFlagsCount: 1,
    nonComplianceFlagsCount: 0,
    confirmedFlagsCount: 5,
    unresolvedFlagsCount: 0,
    processingStatus: "completed",
    primaryRiskReasons: [],
    overallStatus: "Compliant",
    updatedAt: "2026-08-31T04:00:00Z",
  };

  let capturedUrl = "";
  const originalFetch = globalThis.fetch;
  globalThis.fetch = (async (input: RequestInfo | URL) => {
    capturedUrl = String(input);
    return {
      ok: true,
      status: 200,
      statusText: "OK",
      json: async () => [mockSummary],
      text: async () => JSON.stringify([mockSummary]),
    } as Response;
  }) as typeof fetch;

  try {
    const results = await getBidderSummaries({
      tenderId: "t-001",
      status: "compliant",
      sortBy: "compliance_risk",
      sortOrder: "desc",
    });

    if (results.length !== 1 || results[0].bidderName !== "Acme Infrastructure Ltd") {
      throw new Error("Expected getBidderSummaries to return parsed DTO array");
    }

    if (!capturedUrl.includes("/tenders/t-001/bidders/summaries")) {
      throw new Error(`URL missing base path: ${capturedUrl}`);
    }
    if (!capturedUrl.includes("status=compliant")) {
      throw new Error(`URL missing status filter: ${capturedUrl}`);
    }
    if (!capturedUrl.includes("sort_by=compliance_risk")) {
      throw new Error(`URL missing sort_by param: ${capturedUrl}`);
    }
    if (!capturedUrl.includes("sort_order=desc")) {
      throw new Error(`URL missing sort_order param: ${capturedUrl}`);
    }
  } finally {
    globalThis.fetch = originalFetch;
  }

  return true;
}
