"use client";

import { useEffect, useState } from "react";
import { complianceApi, ComplianceFlag } from "../../compliance-flags/api/complianceApi";
import { EvidenceReference } from "../../compliance-flags/components/EvidenceReference";
import { dashboardApi, BidderSummary } from "../../bidder-dashboard/api/dashboardApi";
import { nodeColorMap } from "../../../../packages/ui-kit/tokens/nodeColors";

import { auditApi, AuditEvent } from "../api/auditApi";

interface ReportViewerProps {
  tenderId: string;
  bidderId: string;
}

export function ReportViewer({ tenderId, bidderId }: ReportViewerProps) {
  const [flags, setFlags] = useState<ComplianceFlag[]>([]);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [bidder, setBidder] = useState<BidderSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [fetchedFlags, fetchedBidders, fetchedAudit] = await Promise.all([
          complianceApi.getFlags(tenderId, bidderId),
          dashboardApi.getBidders(tenderId),
          auditApi.getBidderAuditTrail(bidderId)
        ]);
        setFlags(fetchedFlags);
        setBidder(fetchedBidders.find(b => b.id === bidderId) || null);
        setAuditEvents(fetchedAudit);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, [tenderId, bidderId]);

  if (isLoading) return <div className="p-8 text-[var(--color-text-secondary)]">Loading report data...</div>;
  if (error) return <div className="p-8 text-[var(--color-error)]">Error loading report: {error}</div>;

  return (
    <div className="bg-white border border-[var(--color-border)] rounded-md shadow-sm p-8 max-w-5xl mx-auto mb-12">
      {/* Header Section */}
      <div className="border-b border-[var(--color-border)] pb-6 mb-8">
        <h1 className="text-3xl font-bold text-[var(--color-primary)] mb-2">Compliance Audit Report</h1>
        <div className="grid grid-cols-2 gap-4 text-sm text-[var(--color-text-primary)]">
          <div>
            <p className="font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider text-xs mb-1">Bidder Identity</p>
            <p className="text-lg">{bidder?.legal_name || bidderId}</p>
          </div>
          <div>
            <p className="font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider text-xs mb-1">Tender Reference</p>
            <p className="text-lg">{tenderId}</p>
          </div>
        </div>
      </div>

      {/* Flags Section */}
      <div className="space-y-8">
        {flags.length === 0 ? (
          <p className="text-[var(--color-text-secondary)] italic">No compliance flags recorded for this bidder.</p>
        ) : (
          flags.map((flag, idx) => (
            <div key={flag.id} className="border border-[var(--color-border)] rounded-md overflow-hidden print:break-inside-avoid">
              
              {/* Flag Header */}
              <div className="bg-[var(--color-surface-hover)] px-4 py-3 border-b border-[var(--color-border)] flex items-center justify-between">
                <h2 className="font-bold text-[var(--color-text-primary)] text-base">
                  {idx + 1}. {flag.title}
                </h2>
                <span className="text-xs text-[var(--color-text-secondary)] font-mono">ID: {flag.id.slice(0,8)}</span>
              </div>

              {/* Body: Two distinct columns for AI vs Officer */}
              <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-[var(--color-border)]">
                
                {/* Column 1: AI Recommendation */}
                <div className="p-4">
                  <h3 className="text-xs font-bold uppercase tracking-wide text-[var(--color-text-secondary)] mb-3">
                    AI Recommendation
                  </h3>
                  <div className="mb-2">
                    <span 
                      className="inline-block px-2 py-1 text-xs font-bold rounded-sm mb-2"
                      style={{ 
                        backgroundColor: nodeColorMap[flag.status], 
                        color: flag.status === 'VERIFIED' || flag.status === 'NEEDS_REVIEW' || flag.status === 'MISSING' ? 'black' : 'white'
                      }}
                    >
                      {flag.status.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <p className="text-sm text-[var(--color-text-primary)] leading-relaxed mb-4">
                    {flag.ai_recommendation}
                  </p>
                  
                  {/* Evidence References */}
                  {flag.anchors && flag.anchors.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-[var(--color-border)] border-dashed">
                      <p className="text-xs font-bold text-[var(--color-text-secondary)] mb-2">Source Evidence</p>
                      <div className="flex flex-col gap-2">
                        {flag.anchors.map((anchor, i) => (
                          <EvidenceReference key={i} tenderId={tenderId} bidderId={bidderId} anchor={anchor} />
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Column 2: Officer Decision */}
                <div className="p-4 bg-[var(--color-surface)]">
                  <h3 className="text-xs font-bold uppercase tracking-wide text-[var(--color-text-secondary)] mb-3">
                    Final Officer Decision
                  </h3>
                  {(() => {
                    const flagAudit = auditEvents
                      .filter(e => e.flag_id === flag.id && e.action_type === 'decision')
                      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
                    
                    const latestDecision = flagAudit.length > 0 ? flagAudit[0] : null;

                    if (latestDecision) {
                      return (
                        <>
                          <div className="mb-2">
                            <span className="inline-block px-2 py-1 text-xs font-bold rounded-sm border border-[var(--color-border)] bg-white text-black mb-2">
                              {latestDecision.new_state}
                            </span>
                          </div>
                          <div className="text-sm text-[var(--color-text-primary)] leading-relaxed mb-4">
                            <p className="font-semibold text-xs text-[var(--color-text-secondary)] mb-1">Decision Rationale:</p>
                            <p>{latestDecision.notes || "No rationale provided."}</p>
                          </div>
                          <div className="mt-4 pt-4 border-t border-[var(--color-border)] border-dashed text-xs text-[var(--color-text-secondary)]">
                            <p><strong>Recorded By:</strong> {latestDecision.officer_user_id}</p>
                            <p><strong>Recorded At:</strong> {new Date(latestDecision.created_at).toLocaleString()}</p>
                          </div>
                        </>
                      );
                    } else {
                      return (
                        <div className="h-full flex items-center justify-center text-sm text-[var(--color-text-secondary)] italic border-2 border-dashed border-[var(--color-border)] rounded p-4">
                          Pending Review
                        </div>
                      );
                    }
                  })()}
                </div>

              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
