"use client";
import React, { useEffect, useState } from "react";
import { GraphNode, ComplianceFlag } from "@govflow/shared-types";
import { complianceApi } from "../../compliance-flags/api/complianceApi";
import { FlagList } from "../../compliance-flags/components/FlagList";
import { resolveNodeColor } from "../utils/nodeColorMap";
import Link from "next/link";

interface NodeDetailPanelProps {
  node: GraphNode | null;
  tenderId: string;
  bidderId: string;
}

export function NodeDetailPanel({ node, tenderId, bidderId }: NodeDetailPanelProps) {
  const [flags, setFlags] = useState<ComplianceFlag[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadFlags() {
      if (node && node.type === "DOCUMENT" && node.status !== "MISSING") {
        setIsLoading(true);
        try {
          // Fetch all flags for the bidder, then filter for this document
          // In a real optimized system, we might query by documentId directly
          const allFlags = await complianceApi.getFlags(tenderId, bidderId);
          const docId = node.metadata?.documentId;
          const filtered = allFlags.filter(f => f.anchors?.some(a => a.documentId === docId));
          setFlags(filtered);
        } catch (e) {
          console.error("Failed to load flags for document", e);
        } finally {
          setIsLoading(false);
        }
      } else {
        setFlags([]);
      }
    }
    loadFlags();
  }, [node, tenderId, bidderId]);

  if (!node) {
    return (
      <div className="w-96 bg-white border-l border-slate-200 shadow-xl flex flex-col p-6 items-center justify-center text-slate-500 h-full">
        Select a node in the graph to view details.
      </div>
    );
  }

  const isDoc = node.type === "DOCUMENT";
  const statusColors = resolveNodeColor(node.status || "MISSING");

  return (
    <div className="w-96 bg-white border-l border-slate-200 shadow-xl flex flex-col h-full overflow-y-auto">
      <div className="p-6 border-b border-slate-200">
        <h2 className="text-xl font-bold text-[#0C2340] mb-1">{node.label}</h2>
        
        {isDoc ? (
          <div className="mt-4 space-y-4">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase">Status</span>
              <div className="mt-1 flex items-center gap-2">
                <span className={`px-2 py-1 text-xs font-bold rounded ${statusColors.bg} ${statusColors.text} uppercase`}>
                  {(node.status || "MISSING").replace(/_/g, " ")}
                </span>
              </div>
            </div>
            
            {node.status === "MISSING" && (
              <p className="text-sm text-slate-600 bg-slate-50 p-3 rounded border border-slate-200">
                The bidder has not uploaded this required document.
              </p>
            )}

            {node.metadata?.documentId && (
              <div className="mt-6">
                 {/* Navigation to Evidence Viewer */}
                 <Link 
                   href={`/tenders/${tenderId}/bidders/${bidderId}/documents/${node.metadata.documentId}`}
                   className="flex items-center justify-center w-full px-4 py-2 bg-[#F37021] text-white font-medium rounded shadow-sm hover:bg-[#d9621b] transition-colors"
                 >
                   Open Evidence Viewer
                 </Link>
              </div>
            )}
          </div>
        ) : (
          <p className="text-sm text-slate-600 mt-2">Bidder Entity</p>
        )}
      </div>

      {isDoc && node.status !== "MISSING" && (
        <div className="p-6 flex-1 bg-slate-50">
          <h3 className="text-sm font-bold text-slate-700 uppercase tracking-wider mb-4 border-b border-slate-200 pb-2">
            Compliance Flags
          </h3>
          
          {isLoading ? (
            <div className="text-sm text-slate-500">Loading flags...</div>
          ) : (
            <FlagList 
              flags={flags} 
              tenderId={tenderId} 
              onDecisionRecorded={() => {
                // Ideally trigger a refetch of the graph and flags here
                window.location.reload(); 
              }} 
            />
          )}
        </div>
      )}
    </div>
  );
}
