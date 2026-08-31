"use client";
import React, { useEffect, useState } from "react";
import { evidenceApi } from "../api/evidenceApi";
import { ExtractedField, EvidenceAnchor } from "@govflow/shared-types";
import { DocumentPageCanvas } from "./DocumentPageCanvas";
import { AnomalySidePanel } from "./AnomalySidePanel";

interface EvidenceDocumentViewerProps {
  tenderId: string;
  bidderId: string;
  documentId: string;
}

export function EvidenceDocumentViewer({ tenderId, bidderId, documentId }: EvidenceDocumentViewerProps) {
  const [pageNumber, setPageNumber] = useState(1);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  
  const [fields, setFields] = useState<ExtractedField[]>([]);
  const [anchors, setAnchors] = useState<EvidenceAnchor[]>([]);
  
  const [activeOverlayId, setActiveOverlayId] = useState<string | null>(null);
  const [activeType, setActiveType] = useState<"FIELD" | "ANCHOR" | null>(null);
  
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setIsLoading(true);
      setError(null);
      try {
        // 1. Fetch short-lived signed URL for security
        const urlRes = await evidenceApi.getSignedUrl(documentId, pageNumber);
        setPdfUrl(urlRes.url);

        // 2. Fetch overlays for this specific page
        const overlayRes = await evidenceApi.getOverlays(tenderId, bidderId, documentId, pageNumber);
        setFields(overlayRes.fields);
        setAnchors(overlayRes.anchors);
        
      } catch (err: any) {
        console.error(err);
        setError("Failed to load secure document viewer context.");
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [tenderId, bidderId, documentId, pageNumber]);

  const handleOverlayClick = (id: string, type: "FIELD" | "ANCHOR") => {
    setActiveOverlayId(id);
    setActiveType(type);
  };

  // Derive active items to pass to panel
  let activeField = null;
  let activeAnchor = null;

  if (activeType === "FIELD" && activeOverlayId) {
    const idx = parseInt(activeOverlayId.split("-")[1]);
    activeField = fields[idx] || null;
  } else if (activeType === "ANCHOR" && activeOverlayId) {
    const aid = activeOverlayId.replace("anchor-", "");
    activeAnchor = anchors.find(a => a.id === aid) || null;
  }

  if (isLoading && !pdfUrl) {
    return <div className="p-10 text-center">Authenticating Secure Document Viewer...</div>;
  }

  if (error) {
    return <div className="p-10 text-center text-red-600">{error}</div>;
  }

  return (
    <div className="flex w-full h-[calc(100vh-100px)] border-t border-slate-200">
      
      {/* Main Canvas Area */}
      <div className="flex-1 bg-slate-100 overflow-y-auto p-8 flex flex-col items-center">
        
        {/* Pagination Controls */}
        <div className="mb-4 flex items-center gap-4 bg-white px-4 py-2 rounded-full shadow-sm border border-slate-200">
          <button 
            className="text-sm font-semibold text-slate-600 hover:text-slate-900 disabled:opacity-50"
            onClick={() => setPageNumber(p => Math.max(1, p - 1))}
            disabled={pageNumber === 1}
          >
            &larr; Prev
          </button>
          <span className="text-sm font-medium text-slate-500">Page {pageNumber}</span>
          <button 
            className="text-sm font-semibold text-slate-600 hover:text-slate-900"
            onClick={() => setPageNumber(p => p + 1)}
          >
            Next &rarr;
          </button>
        </div>

        {pdfUrl && (
          <div className="w-full max-w-4xl relative">
            <DocumentPageCanvas 
              url={pdfUrl}
              pageNumber={pageNumber}
              fields={fields}
              anchors={anchors}
              activeOverlayId={activeOverlayId}
              onOverlayClick={handleOverlayClick}
            />
          </div>
        )}
      </div>

      {/* Side Panel Area */}
      <AnomalySidePanel 
        activeType={activeType}
        activeField={activeField}
        activeAnchor={activeAnchor}
        tenderId={tenderId}
        bidderId={bidderId}
      />
      
    </div>
  );
}
