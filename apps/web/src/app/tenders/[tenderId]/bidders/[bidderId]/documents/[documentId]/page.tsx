"use client";
import React from "react";
import { useParams, useRouter } from "next/navigation";
import { EvidenceDocumentViewer } from "../../../../../../modules/evidence-viewer/components/EvidenceDocumentViewer";

export default function DocumentViewerPage() {
  const params = useParams();
  const router = useRouter();

  const tenderId = params.tenderId as string;
  const bidderId = params.bidderId as string;
  const documentId = params.documentId as string;

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      
      {/* Viewer Header */}
      <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => router.push(`/tenders/${tenderId}/dashboard?selectedBidder=${bidderId}`)}
            className="text-sm font-semibold text-slate-500 hover:text-slate-800 transition-colors"
          >
            &larr; Back to Dashboard
          </button>
          <div className="h-6 w-px bg-slate-300"></div>
          <div>
            <h1 className="text-lg font-bold text-[#0C2340]">Document Evidence Viewer</h1>
            <p className="text-xs text-slate-500">Document ID: <span className="font-mono">{documentId}</span></p>
          </div>
        </div>
      </header>

      {/* Viewer Workspace */}
      <main className="flex-1 flex overflow-hidden">
        <EvidenceDocumentViewer 
          tenderId={tenderId}
          bidderId={bidderId}
          documentId={documentId}
        />
      </main>
      
    </div>
  );
}