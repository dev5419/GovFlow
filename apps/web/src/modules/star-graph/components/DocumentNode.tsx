import React from "react";
import { Handle, Position } from "@xyflow/react";
import { resolveNodeColor } from "../utils/nodeColorMap";

export function DocumentNode({ data, selected }: any) {
  // Extract canonical status from backend metadata
  const status = data.status || "MISSING";
  const colors = resolveNodeColor(status);
  
  // Selection uses --color-focus (#0C2340) outline.
  const focusStyle = selected 
    ? "ring-2 ring-[#0C2340] ring-offset-2" 
    : "";

  return (
    <div className={`bg-white rounded shadow-sm p-3 border-2 ${colors.border} ${focusStyle} min-w-[120px] max-w-[180px] text-center transition-all cursor-pointer`}>
      <Handle type="target" position={Position.Left} className="!bg-[#0C2340] !w-2 !h-2" />
      <Handle type="target" position={Position.Top} className="!bg-[#0C2340] !w-2 !h-2" />
      <Handle type="target" position={Position.Right} className="!bg-[#0C2340] !w-2 !h-2" />
      <Handle type="target" position={Position.Bottom} className="!bg-[#0C2340] !w-2 !h-2" />
      
      {/* Node label is exactly the canonical requirement (e.g. GST Certificate) */}
      <h4 className="text-xs font-bold text-slate-800 break-words leading-tight">{data.label}</h4>
      
      {/* Status indicator bar using mapped colors */}
      <div className={`mt-2 h-1.5 w-full rounded-full ${colors.bg}`}></div>
      <p className={`mt-1 text-[10px] font-semibold uppercase tracking-wider ${colors.text}`}>
        {status.replace(/_/g, " ")}
      </p>
    </div>
  );
}
