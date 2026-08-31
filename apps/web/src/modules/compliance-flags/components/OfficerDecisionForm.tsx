"use client";
import React, { useState, useRef, useEffect } from "react";
import { ComplianceFlag } from "@govflow/shared-types";

interface OfficerDecisionFormProps {
  flag: ComplianceFlag;
  onDecisionSubmit: (decisionState: string, notes: string) => Promise<void>;
}

export function OfficerDecisionForm({ flag, onDecisionSubmit }: OfficerDecisionFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  
  // Dialog State
  const [dialogOpen, setDialogOpen] = useState(false);
  const [pendingDecision, setPendingDecision] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (dialogOpen) {
      dialogRef.current?.showModal();
    } else {
      dialogRef.current?.close();
    }
  }, [dialogOpen]);

  const handleActionClick = (decision: string) => {
    setPendingDecision(decision);
    setNotes("");
    setError("");
    setDialogOpen(true);
  };

  const closeDialog = () => {
    setDialogOpen(false);
    setPendingDecision(null);
  };

  const handleSubmit = async () => {
    if (!pendingDecision) return;
    
    const needsNotes = ["Rejected", "Overridden", "Escalated"].includes(pendingDecision);
    if (needsNotes && !notes.trim()) {
      setError(`Notes are legally required to record an '${pendingDecision}' decision.`);
      return;
    }

    try {
      setIsSubmitting(true);
      await onDecisionSubmit(pendingDecision, notes);
      closeDialog();
    } catch (err: any) {
      setError(err.message || "Failed to record decision.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-50 border border-slate-200 p-4 rounded-md">
      {/* 
        PRD §6.2 / §20.4 constraint: The original AI recommendation MUST 
        be prominently visible alongside the decision controls. 
      */}
      <div className="mb-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-r-md">
        <h4 className="text-sm font-semibold text-blue-900 mb-1">Original AI Finding</h4>
        <p className="text-sm text-blue-800">{flag.aiRecommendation}</p>
      </div>

      <div className="flex flex-wrap gap-2 items-center">
        {/* Primary Action - Uses Primary Button Spec (--color-accent #F37021) */}
        <button
          onClick={() => handleActionClick("Confirmed")}
          className="px-4 py-2 bg-[#F37021] text-white text-sm font-medium rounded hover:bg-[#d9621b] transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-[#F37021]"
        >
          Confirm Finding
        </button>

        {/* Secondary Actions - Transparent BG, #0C2340 border/text */}
        <button
          onClick={() => handleActionClick("Rejected")}
          className="px-4 py-2 bg-transparent text-[#0C2340] border border-[#0C2340] text-sm font-medium rounded hover:bg-slate-100 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-[#0C2340]"
        >
          Reject
        </button>

        <button
          onClick={() => handleActionClick("Overridden")}
          className="px-4 py-2 bg-transparent text-[#0C2340] border border-[#0C2340] text-sm font-medium rounded hover:bg-slate-100 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-[#0C2340]"
        >
          Override
        </button>

        <button
          onClick={() => handleActionClick("Escalated")}
          className="px-4 py-2 bg-transparent text-[#0C2340] border border-[#0C2340] text-sm font-medium rounded hover:bg-slate-100 transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-[#0C2340]"
        >
          Escalate
        </button>
      </div>

      {/* WCAG 2.1 AA Compliant Confirmation Dialog */}
      <dialog 
        ref={dialogRef} 
        className="p-6 rounded-md shadow-xl backdrop:bg-slate-900/50 max-w-md w-full border border-slate-200"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
        onCancel={closeDialog}
      >
        <h2 id="dialog-title" className="text-lg font-semibold text-slate-900 mb-2">
          Confirm Decision: {pendingDecision}
        </h2>
        <p id="dialog-description" className="text-sm text-slate-600 mb-4">
          You are about to record this decision on the bidder's compliance record. This action is audited and final.
        </p>

        {pendingDecision && ["Rejected", "Overridden", "Escalated"].includes(pendingDecision) && (
          <div className="mb-4">
            <label htmlFor="decision-notes" className="block text-sm font-medium text-slate-700 mb-1">
              Officer Notes (Required)
            </label>
            <textarea
              id="decision-notes"
              className="w-full border border-slate-300 rounded-md p-2 text-sm focus:ring-[#0C2340] focus:border-[#0C2340]"
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={`Provide a formal reason for ${pendingDecision.toLowerCase()} this finding...`}
              required
              aria-required="true"
            />
          </div>
        )}
        
        {/* For Confirmed, notes are optional */}
        {pendingDecision === "Confirmed" && (
          <div className="mb-4">
            <label htmlFor="decision-notes" className="block text-sm font-medium text-slate-700 mb-1">
              Officer Notes (Optional)
            </label>
            <textarea
              id="decision-notes"
              className="w-full border border-slate-300 rounded-md p-2 text-sm focus:ring-[#0C2340] focus:border-[#0C2340]"
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Additional context..."
            />
          </div>
        )}

        {error && (
          <div className="mb-4 p-2 bg-red-50 text-red-700 text-sm rounded-md border border-red-200" role="alert">
            {error}
          </div>
        )}

        <div className="flex justify-end gap-2 mt-6">
          <button
            type="button"
            onClick={closeDialog}
            disabled={isSubmitting}
            className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-md transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="px-4 py-2 bg-[#0C2340] text-white text-sm font-medium rounded-md hover:bg-[#1a365d] transition-colors disabled:opacity-50"
          >
            {isSubmitting ? "Recording..." : "Record Decision"}
          </button>
        </div>
      </dialog>
    </div>
  );
}
