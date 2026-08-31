import React from "react";
import { Handle, Position } from "@xyflow/react";

export function BidderNode({ data, selected }: any) {
  // PRD §14, Design.md: --color-surface (#FFFFFF), 1px border, 4px radius. 
  // No glassmorphism, flat fills only.
  // Selection uses --color-focus (#0C2340) outline.
  
  const borderStyle = selected 
    ? "border-[#0C2340] ring-2 ring-[#0C2340] ring-offset-1" 
    : "border-[#DDE2E5]";

  return (
    <div className={`bg-white rounded shadow-sm px-6 py-4 border ${borderStyle} min-w-[150px] text-center`}>
      {/* Target handle handles inbound edges if any, though bidder is usually a source */}
      <Handle type="target" position={Position.Top} className="opacity-0" />
      
      <h3 className="text-sm font-semibold text-slate-900 mb-1">Bidder</h3>
      <p className="text-base font-bold text-slate-800">{data.label}</p>
      
      {/* Source handles in all directions for star topology */}
      <Handle type="source" position={Position.Top} id="top" className="opacity-0" />
      <Handle type="source" position={Position.Right} id="right" className="opacity-0" />
      <Handle type="source" position={Position.Bottom} id="bottom" className="opacity-0" />
      <Handle type="source" position={Position.Left} id="left" className="opacity-0" />
    </div>
  );
}
