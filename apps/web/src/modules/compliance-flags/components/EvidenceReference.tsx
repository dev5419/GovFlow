import React from "react";
import Link from "next/link";
import { EvidenceAnchor } from "@govflow/shared-types";

interface EvidenceReferenceProps {
  tenderId: string;
  anchor: EvidenceAnchor;
}

export function EvidenceReference({ tenderId, anchor }: EvidenceReferenceProps) {
  // Renders a clickable link to the Evidence Viewer (Module 6)
  return (
    <div className="text-sm">
      <Link 
        href={`/tenders/${tenderId}/evidence?documentId=${anchor.documentId}&page=${anchor.pageNumber}&anchorId=${anchor.id}`}
        className="text-blue-600 hover:text-blue-800 hover:underline flex items-center gap-1"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
        Document {anchor.documentId.substring(0, 8)} (Page {anchor.pageNumber})
      </Link>
    </div>
  );
}
