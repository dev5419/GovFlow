import React from "react";
import { nodeColors } from "@govflow/ui-kit/tokens/nodeColors";

interface BoundingBoxOverlayProps {
  id: string;
  left: string;
  top: string;
  width: string;
  height: string;
  status: "VERIFIED" | "NEEDS_REVIEW" | "INSUFFICIENT_EVIDENCE" | "POTENTIAL_NON_COMPLIANCE" | "CONFIRMED_NON_COMPLIANCE" | "SELECTED";
  onClick: (id: string) => void;
}

export function BoundingBoxOverlay({ id, left, top, width, height, status, onClick }: BoundingBoxOverlayProps) {
  let colorTokens = nodeColors.verified;
  
  if (status === "SELECTED") {
    // PRD 8.6 dictates blue for currently selected
    colorTokens = {
      bg: "bg-blue-500",
      text: "text-blue-800",
      border: "border-blue-600",
      hex: "#3b82f6"
    };
  } else if (status === "POTENTIAL_NON_COMPLIANCE" || status === "CONFIRMED_NON_COMPLIANCE") {
    colorTokens = nodeColors.nonCompliant;
  } else if (status === "NEEDS_REVIEW" || status === "INSUFFICIENT_EVIDENCE") {
    colorTokens = nodeColors.needsReview;
  }

  // 15-20% opacity fill to preserve legibility of underlying text per PRD
  // Using arbitrary tailwind opacity values or inline styles
  
  return (
    <div
      onClick={(e) => {
        e.stopPropagation();
        onClick(id);
      }}
      className={`absolute cursor-pointer border-2 transition-colors ${colorTokens.border}`}
      style={{
        left,
        top,
        width,
        height,
        backgroundColor: `${colorTokens.hex}33`, // 20% opacity in hex (33)
      }}
    >
      {/* Invisible accessible text for screen readers could go here if we had semantic labels per box */}
    </div>
  );
}
