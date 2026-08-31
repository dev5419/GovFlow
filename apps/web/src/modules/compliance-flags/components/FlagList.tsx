"use client";
import React from "react";
import { ComplianceFlag } from "@govflow/shared-types";
import { FlagBadge } from "./FlagBadge";
import { EvidenceReference } from "./EvidenceReference";
import { OfficerDecisionForm } from "./OfficerDecisionForm";
import { complianceApi } from "../api/complianceApi";

interface FlagListProps {
  flags: ComplianceFlag[];
  tenderId: string;
  onDecisionRecorded: () => void; // Callback to refresh data after decision
}

export function FlagList({ flags, tenderId, onDecisionRecorded }: FlagListProps) {
  const handleDecisionSubmit = async (flagId: string, decisionState: string, notes: string) => {
    await complianceApi.recordDecision(flagId, decisionState, notes);
    onDecisionRecorded();
  };

  if (!flags || flags.length === 0) {
    return (
      <div className="p-8 text-center bg-slate-50 border border-slate-200 rounded-lg text-slate-500">
        No compliance flags found.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {flags.map((flag) => (
        <div key={flag.id} className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
          {/* Header */}
          <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
            <div className="flex items-center gap-3">
              <FlagBadge status={flag.status} />
              <h3 className="text-lg font-semibold text-slate-900">{flag.title}</h3>
            </div>
            <div className="text-xs text-slate-500 font-medium">
              Severity: <span className="uppercase">{flag.severity}</span>
            </div>
          </div>
          
          {/* Body */}
          <div className="p-6">
            <div className="mb-6">
              <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Reason</h4>
              <p className="text-sm text-slate-800 leading-relaxed">{flag.reason}</p>
            </div>

            {/* Evidence Links */}
            {flag.anchors && flag.anchors.length > 0 && (
              <div className="mb-6">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Evidence</h4>
                <div className="flex flex-col gap-2">
                  {flag.anchors.map((anchor) => (
                    <EvidenceReference key={anchor.id} tenderId={tenderId} anchor={anchor} />
                  ))}
                </div>
              </div>
            )}

            {/* Officer Decision Controls */}
            <div className="mt-6 pt-6 border-t border-slate-100">
              <OfficerDecisionForm 
                flag={flag} 
                onDecisionSubmit={(decision, notes) => handleDecisionSubmit(flag.id, decision, notes)} 
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
