import React from "react";
import Link from "next/link";
import { ArrowRight, ShieldCheck, FileSpreadsheet, GitBranch, ShieldAlert } from "lucide-react";

export default function Home() {
  const defaultTenderId = "tender-001";

  return (
    <div className="min-h-screen bg-[#F8F9FA] flex flex-col">
      {/* Institutional Top Header */}
      <header
        className="w-full border-b border-[#1B365D]"
        style={{ backgroundColor: "var(--color-primary, #0C2340)" }}
      >
        <div className="gov-container py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ShieldCheck size={28} className="text-[#F37021]" aria-hidden="true" />
            <div>
              <span className="text-lg font-bold text-white tracking-wide block">
                GovFlow
              </span>
              <span className="text-[11px] text-[#DDE2E5] block">
                Public Procurement Compliance & Verification Platform
              </span>
            </div>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-[#1B365D] text-white border border-[#2A4B7C] font-semibold">
            Institutional Portal
          </span>
        </div>
      </header>

      {/* Main Hero / Portal Navigation */}
      <main className="gov-container flex-1 py-12">
        <div className="max-w-3xl">
          <span className="text-xs font-bold uppercase tracking-wider text-[#F37021] block mb-2">
            Procurement Officer Workspace
          </span>
          <h1
            className="text-3xl md:text-4xl font-bold tracking-tight mb-4"
            style={{ color: "var(--color-primary, #0C2340)" }}
          >
            Tender Verification & Bid Evaluation
          </h1>
          <p className="text-base text-[#595959] leading-relaxed mb-8">
            Access pre-aggregated compliance assessments, interactive bidder-document
            graphs, bounding-box evidence overlays, and audit-logged decision workflows
            for active government tenders.
          </p>

          {/* Active Tender Cards */}
          <div className="gov-card p-6 mb-8 border border-[#DDE2E5]">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[11px] font-bold uppercase px-2 py-0.5 rounded bg-[#E8F5E9] text-[#138808] border border-[#C8E6C9]">
                  Active Tender
                </span>
                <h2
                  className="text-lg font-bold mt-2 mb-1"
                  style={{ color: "var(--color-primary, #0C2340)" }}
                >
                  Highway Expansion Project — Package 4
                </h2>
                <p className="text-xs text-[#595959] m-0">
                  Ref: GEM/2026/B/894210 • Tender ID: <span className="font-mono">{defaultTenderId}</span>
                </p>
              </div>

              <Link
                href={`/tenders/${defaultTenderId}/dashboard`}
                className="gov-btn-primary self-start sm:self-center"
                style={{
                  backgroundColor: "var(--color-accent, #F37021)",
                  color: "#FFFFFF",
                  padding: "10px 20px",
                  fontSize: "14px",
                }}
              >
                <span>Open Dashboard</span>
                <ArrowRight size={16} aria-hidden="true" />
              </Link>
            </div>
          </div>

          {/* Feature Highlights Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="gov-card p-4">
              <FileSpreadsheet size={20} className="text-[#0C2340] mb-2" aria-hidden="true" />
              <h3 className="text-sm font-bold text-[#0C2340] mb-1">
                F-01 Bidder Dashboard
              </h3>
              <p className="text-xs text-[#595959] m-0">
                Aggregated compliance scores, document counts, and primary risk findings.
              </p>
            </div>

            <div className="gov-card p-4">
              <GitBranch size={20} className="text-[#0C2340] mb-2" aria-hidden="true" />
              <h3 className="text-sm font-bold text-[#0C2340] mb-1">
                F-05 Star Graph
              </h3>
              <p className="text-xs text-[#595959] m-0">
                Interactive topological visualization connecting bidders, documents, and rules.
              </p>
            </div>

            <div className="gov-card p-4">
              <ShieldAlert size={20} className="text-[#0C2340] mb-2" aria-hidden="true" />
              <h3 className="text-sm font-bold text-[#0C2340] mb-1">
                F-06 Evidence Viewer
              </h3>
              <p className="text-xs text-[#595959] m-0">
                Page-level coordinate bounding boxes linking contradictory statements.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Institutional Footer */}
      <footer
        className="w-full py-4 border-t border-[#DDE2E5] bg-white text-xs text-[#595959]"
      >
        <div className="gov-container flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>GovFlow Procurement Verification System • WCAG 2.1 AA Compliant</span>
          <span>Security Classification: Restricted / Internal Government Use</span>
        </div>
      </footer>
    </div>
  );
}
