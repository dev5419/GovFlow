import React from "react";
import { nodeColors } from "@govflow/ui-kit/tokens/nodeColors";

export function GraphLegend() {
  const legendItems = [
    { label: "Processing", colors: nodeColors.missing }, // Processing is often slate/blue, let's use missing/slate for now or define a processing color. Wait, we mapped processing to missing if missing is missing. Let's add a specific mapping in legend.
    { label: "Missing", colors: nodeColors.missing },
    { label: "Non-Compliance", colors: nodeColors.nonCompliant },
    { label: "Needs Review", colors: nodeColors.needsReview },
    { label: "Verified", colors: nodeColors.verified },
  ];

  return (
    <div className="absolute bottom-4 left-4 bg-white border border-slate-200 rounded-md shadow-sm p-3 z-10 w-48 pointer-events-auto" role="complementary" aria-label="Graph Color Legend">
      <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 border-b border-slate-100 pb-1">Legend</h4>
      <ul className="space-y-1.5 text-xs text-slate-600">
        <li className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full bg-slate-300 border border-slate-400`}></span>
           <span>Processing</span>
        </li>
        <li className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full ${nodeColors.missing.bg} ${nodeColors.missing.border} border`}></span>
           <span>Missing</span>
        </li>
        <li className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full ${nodeColors.nonCompliant.bg} ${nodeColors.nonCompliant.border} border`}></span>
           <span>Non-Compliance</span>
        </li>
        <li className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full ${nodeColors.needsReview.bg} ${nodeColors.needsReview.border} border`}></span>
           <span>Needs Review</span>
        </li>
        <li className="flex items-center gap-2">
           <span className={`w-3 h-3 rounded-full ${nodeColors.verified.bg} ${nodeColors.verified.border} border`}></span>
           <span>Verified</span>
        </li>
      </ul>
    </div>
  );
}
