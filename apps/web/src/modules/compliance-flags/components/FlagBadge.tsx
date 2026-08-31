import React from "react";
import { getStatusColors } from "@govflow/ui-kit/tokens/nodeColors";

interface FlagBadgeProps {
  status: string;
  label?: string;
}

export function FlagBadge({ status, label }: FlagBadgeProps) {
  const colors = getStatusColors(status);
  const displayLabel = label || status.replace(/_/g, " ");

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${colors.bg} ${colors.text} ${colors.border}`}
    >
      {displayLabel}
    </span>
  );
}
