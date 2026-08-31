"use client";

import { useState, useEffect } from "react";
import { reportApi, ReportData } from "../api/reportApi";
import { Download, Loader2, FileText } from "lucide-react";

interface DownloadReportButtonProps {
  tenderId: string;
  bidderId: string;
}

export function DownloadReportButton({ tenderId, bidderId }: DownloadReportButtonProps) {
  const [latestReport, setLatestReport] = useState<ReportData | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch initial report status
  useEffect(() => {
    fetchLatestReport();
  }, [tenderId, bidderId]);

  // Poll if there's a PENDING report
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPolling) {
      interval = setInterval(() => {
        fetchLatestReport();
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [isPolling]);

  const fetchLatestReport = async () => {
    try {
      const reports = await reportApi.getReports(tenderId, bidderId);
      if (reports && reports.length > 0) {
        // Find the most recently requested report
        const sorted = reports.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        const latest = sorted[0];
        setLatestReport(latest);

        if (latest.status === "PENDING") {
          setIsPolling(true);
        } else {
          setIsPolling(false);
        }
      }
    } catch (err: any) {
      console.error("Failed to fetch reports", err);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    try {
      await reportApi.generateReport(tenderId, bidderId);
      // Immediately start polling after request
      setIsPolling(true);
    } catch (err: any) {
      setError(err.message);
      setIsGenerating(false);
    }
  };

  if (error) {
    return (
      <div className="flex items-center gap-2 text-sm text-[var(--color-error)] print:hidden">
        <span>Failed to generate report.</span>
        <button onClick={handleGenerate} className="underline">Retry</button>
      </div>
    );
  }

  if (isPolling || isGenerating || latestReport?.status === "PENDING") {
    return (
      <button 
        disabled
        className="print:hidden flex items-center gap-2 bg-slate-100 text-slate-500 font-semibold py-2 px-4 rounded-md border border-slate-200 cursor-not-allowed"
      >
        <Loader2 className="w-4 h-4 animate-spin" />
        Generating PDF...
      </button>
    );
  }

  if (latestReport?.status === "COMPLETED" && latestReport.download_url) {
    return (
      <div className="print:hidden flex items-center gap-3">
        <a 
          href={latestReport.download_url} 
          target="_blank" 
          rel="noreferrer"
          className="flex items-center gap-2 bg-[var(--color-primary)] hover:bg-[#0a1d35] text-white font-semibold py-2 px-4 rounded-md transition-colors"
        >
          <Download className="w-4 h-4" />
          Download PDF
        </a>
        <button 
          onClick={handleGenerate}
          className="text-xs text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] underline"
        >
          Generate New Version
        </button>
      </div>
    );
  }

  return (
    <button 
      onClick={handleGenerate}
      className="print:hidden flex items-center gap-2 bg-[var(--color-primary)] hover:bg-[#0a1d35] text-white font-semibold py-2 px-4 rounded-md transition-colors"
    >
      <FileText className="w-4 h-4" />
      Generate PDF Report
    </button>
  );
}
