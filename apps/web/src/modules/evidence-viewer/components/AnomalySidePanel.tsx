"use client";
import React from "react";
import { ExtractedField, EvidenceAnchor } from "@govflow/shared-types";
import { LinkedEvidencePanel } from "./LinkedEvidencePanel";

interface AnomalySidePanelProps {
  activeType: "FIELD" | "ANCHOR" | null;
  activeField: ExtractedField | null;
  activeAnchor: EvidenceAnchor | null;
  tenderId: string;
  bidderId: string;
}

export function AnomalySidePanel({ activeType, activeField, activeAnchor, tenderId, bidderId }: AnomalySidePanelProps) {
  
  if (!activeType) {
    return (
      <div className="w-96 bg-[#F1F4F8] border-l border-slate-200 shadow-inner flex flex-col p-6 items-center justify-center text-slate-500 h-full">
        <p className="text-sm text-center">Select a highlighted bounding box on the document to view extraction details or compliance flags.</p>
      </div>
    );
  }

  // PRD §8.6: WCAG 2.1 AA requires non-color indicators.
  // We use explicit icons/text to convey status alongside color.
  
  return (
    <div className="w-96 bg-[#F1F4F8] border-l border-slate-200 shadow-inner flex flex-col h-full overflow-y-auto">
      <div className="p-6">
        
        {activeType === "FIELD" && activeField && (
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xl" aria-hidden="true">✅</span>
              <h2 className="text-lg font-bold text-slate-800">Verified Extraction</h2>
            </div>
            
            <div className="space-y-4 bg-white p-4 rounded border border-slate-200 shadow-sm">
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Field Name</span>
                <span className="block text-sm font-medium text-slate-900 mt-1">{activeField.canonical_name}</span>
              </div>
              
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Extracted Value</span>
                <span className="block text-base font-bold text-slate-900 mt-1 bg-slate-50 p-2 border border-slate-100 rounded">
                  {activeField.raw_value}
                </span>
              </div>
              
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Confidence</span>
                {/* Always show numeric confidence per PRD design rules */}
                <span className="block text-sm font-medium text-slate-900 mt-1">
                  {(activeField.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>
        )}

        {activeType === "ANCHOR" && activeAnchor && (
          <div>
             <div className="flex items-center gap-2 mb-4">
              <span className="text-xl" aria-hidden="true">⚠️</span>
              <h2 className="text-lg font-bold text-red-700">Compliance Anomaly</h2>
            </div>
            
            <div className="space-y-4 bg-white p-4 rounded border border-red-200 shadow-sm">
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">Flagged Snippet</span>
                <span className="block text-base font-bold text-slate-900 mt-1 bg-red-50 p-2 border border-red-100 rounded">
                  {activeAnchor.snippet}
                </span>
              </div>
              
              <div>
                <span className="block text-xs font-semibold text-slate-500 uppercase">OCR Confidence</span>
                <span className="block text-sm font-medium text-slate-900 mt-1">
                  {(activeAnchor.confidence * 100).toFixed(1)}%
                </span>
              </div>
              
              {/* If this anchor belongs to a specific flag, we would normally pass the flagId down. 
                  For demonstration of the module link, we assume flagId is available or we search for it.
                  If available, we render LinkedEvidencePanel. */}
              
              <LinkedEvidencePanel 
                flagId="flag_placeholder_id" 
                sourceAnchorId={activeAnchor.id} 
                tenderId={tenderId}
                bidderId={bidderId}
              />
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
}
