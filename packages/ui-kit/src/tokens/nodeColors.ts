/**
 * Centralized semantic color tokens for status indicators, badges, and graphs.
 * Maps GovFlow compliance statuses to the PRD §8.5 design specifications.
 */

export const nodeColors = {
  verified: {
    bg: "bg-emerald-100",
    text: "text-emerald-800",
    border: "border-emerald-200",
    hex: "#10B981", // Emerald 500 for graph nodes
  },
  needsReview: {
    bg: "bg-amber-100",
    text: "text-amber-800",
    border: "border-amber-200",
    hex: "#F59E0B", // Amber 500 for graph nodes
  },
  nonCompliant: {
    bg: "bg-red-100",
    text: "text-red-800",
    border: "border-red-200",
    hex: "#EF4444", // Red 500 for graph nodes
  },
  missing: {
    bg: "bg-slate-100",
    text: "text-slate-800",
    border: "border-slate-200",
    hex: "#64748B", // Slate 500 for graph nodes
  },
};

/**
 * Helper to map a raw ComplianceFlagStatus from the backend to a color profile.
 */
export const getStatusColors = (status: string) => {
  switch (status) {
    case "VERIFIED":
      return nodeColors.verified;
    case "NEEDS_REVIEW":
    case "INSUFFICIENT_EVIDENCE":
      return nodeColors.needsReview;
    case "POTENTIAL_NON_COMPLIANCE":
    case "CONFIRMED_NON_COMPLIANCE":
      return nodeColors.nonCompliant;
    case "MISSING":
      return nodeColors.missing;
    default:
      return nodeColors.missing;
  }
};
