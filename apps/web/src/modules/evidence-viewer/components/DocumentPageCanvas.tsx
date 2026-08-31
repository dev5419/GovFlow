"use client";
import React, { useRef, useEffect, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import { BoundingBoxOverlay } from "./BoundingBoxOverlay";
import { scaleCoordinates } from "../utils/coordinateScaler";
import { ExtractedField, EvidenceAnchor } from "@govflow/shared-types";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";

// Set worker path for react-pdf
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface DocumentPageCanvasProps {
  url: string;
  pageNumber: number;
  fields: ExtractedField[];
  anchors: EvidenceAnchor[];
  activeOverlayId: string | null;
  onOverlayClick: (id: string, type: "FIELD" | "ANCHOR") => void;
}

export function DocumentPageCanvas({ url, pageNumber, fields, anchors, activeOverlayId, onOverlayClick }: DocumentPageCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerWidth, setContainerWidth] = useState<number>(800);

  // ResizeObserver to track actual DOM width for scaling
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setContainerWidth(entry.contentRect.width);
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={containerRef} className="relative w-full shadow-lg border border-slate-200 bg-white">
      <Document
        file={url}
        loading={<div className="p-10 text-center text-slate-500">Loading Document...</div>}
        error={<div className="p-10 text-center text-red-500">Failed to load PDF. Please ensure you have access.</div>}
      >
        <Page
          pageNumber={pageNumber}
          width={containerWidth} // React-pdf will automatically scale the height to preserve aspect ratio
          renderTextLayer={false}
          renderAnnotationLayer={false}
        />
      </Document>

      {/* Render Overlays on top of the PDF canvas */}
      <div className="absolute inset-0 z-10 pointer-events-none">
        {fields.map((f, idx) => {
          if (!f.bounding_box) return null;
          const scaled = scaleCoordinates(f.bounding_box);
          // By default, generic extracted fields are "verified" unless they are part of a flag (anchor)
          const isSelected = activeOverlayId === `field-${idx}`;
          return (
            <div className="pointer-events-auto" key={`field-${idx}`}>
              <BoundingBoxOverlay
                id={`field-${idx}`}
                left={scaled.left}
                top={scaled.top}
                width={scaled.width}
                height={scaled.height}
                status={isSelected ? "SELECTED" : "VERIFIED"}
                onClick={() => onOverlayClick(`field-${idx}`, "FIELD")}
              />
            </div>
          );
        })}

        {anchors.map((a) => {
          if (!a.boundingBox) return null;
          const scaled = scaleCoordinates(a.boundingBox);
          const isSelected = activeOverlayId === `anchor-${a.id}`;
          // For simplicity, we assume an anchor is non-compliant or needs review.
          // The actual status would come from the parent Flag, but we'll use a heuristic for the visual if not passed down.
          // Ideally, we pass the flag status down. For now, we'll assume it's a conflict (RED) if not selected.
          return (
             <div className="pointer-events-auto" key={`anchor-${a.id}`}>
               <BoundingBoxOverlay
                 id={`anchor-${a.id}`}
                 left={scaled.left}
                 top={scaled.top}
                 width={scaled.width}
                 height={scaled.height}
                 status={isSelected ? "SELECTED" : "POTENTIAL_NON_COMPLIANCE"}
                 onClick={() => onOverlayClick(`anchor-${a.id}`, "ANCHOR")}
               />
             </div>
          );
        })}
      </div>
    </div>
  );
}
