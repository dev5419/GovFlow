"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { EvidenceAnchor } from "@govflow/shared-types";
import { evidenceApi } from "../api/evidenceApi";

interface LinkedEvidencePanelProps {
  flagId: string;
  sourceAnchorId: string;
  tenderId: string;
  bidderId: string;
}

export function LinkedEvidencePanel({ flagId, sourceAnchorId, tenderId, bidderId }: LinkedEvidencePanelProps) {
  const [linkedAnchors, setLinkedAnchors] = useState<EvidenceAnchor[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadLinked() {
      setIsLoading(true);
      try {
        const response = await evidenceApi.getLinkedEvidence(flagId, sourceAnchorId);
        setLinkedAnchors(response.linked_anchors);
      } catch (e) {
        console.error("Failed to load linked evidence", e);
      } finally {
        setIsLoading(false);
      }
    }
    loadLinked();
  }, [flagId, sourceAnchorId]);

  if (isLoading) {
    return <div className="text-xs text-slate-500 mt-4">Checking for cross-document contradictions...</div>;
  }

  if (linkedAnchors.length === 0) return null;

  return (
    <div className="mt-6 border-t border-slate-200 pt-4">
      <h4 className="text-sm font-bold text-slate-800 mb-2 flex items-center gap-2">
        <span>🔗</span> Linked Contradictions
      </h4>
      <p className="text-xs text-slate-600 mb-3">
        This evidence conflicts with data extracted from other documents.
      </p>
      
      <ul className="space-y-2">
        {linkedAnchors.map((anchor) => (
          <li key={anchor.id}>
            <Link 
              href={`/tenders/${tenderId}/bidders/${bidderId}/documents/${anchor.documentId}`}
              className="block p-3 bg-white border border-red-200 rounded text-sm hover:border-red-400 hover:shadow-sm transition-all"
            >
              <div className="font-semibold text-red-700">Conflicting Anchor</div>
              <div className="text-xs text-slate-500 mt-1 truncate">"{anchor.snippet}"</div>
              <div className="text-xs font-medium text-blue-600 mt-2">View Document &rarr;</div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
