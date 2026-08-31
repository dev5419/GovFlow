"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import type { BidderComplianceSummary } from "@govflow/shared-types";
import {
  getBidderSummaries,
  type GetBidderSummariesParams,
} from "../api/dashboardApi";

export interface UseBidderListOptions {
  initialStatus?: string;
  initialSortBy?: "compliance_risk" | "missing_documents" | "processing_status";
  initialSortOrder?: "asc" | "desc";
  autoRefreshIntervalMs?: number;
}

export interface UseBidderListReturn {
  data: BidderComplianceSummary[];
  isLoading: boolean;
  isRefetching: boolean;
  error: Error | null;
  statusFilter: string;
  sortBy: "compliance_risk" | "missing_documents" | "processing_status" | undefined;
  sortOrder: "asc" | "desc";
  setStatusFilter: (status: string) => void;
  setSortBy: (
    sortBy:
      | "compliance_risk"
      | "missing_documents"
      | "processing_status"
      | undefined
  ) => void;
  setSortOrder: (order: "asc" | "desc") => void;
  refetch: () => Promise<void>;
  lastFetchedAt: Date | null;
}

export function useBidderList(
  tenderId: string,
  options: UseBidderListOptions = {}
): UseBidderListReturn {
  const {
    initialStatus = "all",
    initialSortBy,
    initialSortOrder = "asc",
    autoRefreshIntervalMs,
  } = options;

  const [data, setData] = useState<BidderComplianceSummary[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefetching, setIsRefetching] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>(initialStatus);
  const [sortBy, setSortBy] = useState<
    "compliance_risk" | "missing_documents" | "processing_status" | undefined
  >(initialSortBy);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">(initialSortOrder);
  const [lastFetchedAt, setLastFetchedAt] = useState<Date | null>(null);

  const isMountedRef = useRef(true);

  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const fetchData = useCallback(
    async (isBackground: boolean = false) => {
      if (!tenderId) return;

      if (isBackground) {
        setIsRefetching(true);
      } else {
        setIsLoading(true);
      }
      setError(null);

      try {
        const params: GetBidderSummariesParams = {
          tenderId,
          status: statusFilter === "all" ? undefined : statusFilter,
          sortBy,
          sortOrder,
        };

        const result = await getBidderSummaries(params);
        if (isMountedRef.current) {
          setData(result);
          setLastFetchedAt(new Date());
        }
      } catch (err) {
        if (isMountedRef.current) {
          setError(
            err instanceof Error
              ? err
              : new Error("An unexpected error occurred while fetching bidder list")
          );
        }
      } finally {
        if (isMountedRef.current) {
          setIsLoading(false);
          setIsRefetching(false);
        }
      }
    },
    [tenderId, statusFilter, sortBy, sortOrder]
  );

  useEffect(() => {
    fetchData(false);
  }, [fetchData]);

  // Optional auto-refresh interval for live processing updates per PRD §8.1
  useEffect(() => {
    if (!autoRefreshIntervalMs || autoRefreshIntervalMs <= 0) return;

    const interval = setInterval(() => {
      fetchData(true);
    }, autoRefreshIntervalMs);

    return () => clearInterval(interval);
  }, [autoRefreshIntervalMs, fetchData]);

  const refetch = useCallback(async () => {
    await fetchData(true);
  }, [fetchData]);

  return {
    data,
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
  };
}
