import React from "react";
import type { Metadata } from "next";
import { BidderListDashboard } from "@/modules/bidder-dashboard";

interface PageProps {
  params: Promise<{
    tenderId: string;
  }>;
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { tenderId } = await params;
  return {
    title: `Bidder Compliance Dashboard — Tender ${tenderId} | GovFlow`,
    description: `Pre-aggregated compliance overview and risk assessment for Tender ${tenderId}`,
  };
}

export default async function TenderDashboardPage({ params }: PageProps) {
  const { tenderId } = await params;

  return (
    <BidderListDashboard
      tenderId={tenderId}
      tenderTitle="Highway Expansion Project — Package 4"
      tenderNumber={`GEM/2026/B/${tenderId.substring(0, 8).toUpperCase()}`}
    />
  );
}