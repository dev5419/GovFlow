import { getStatusColors } from "@govflow/ui-kit/tokens/nodeColors";

/**
 * A thin wrapper mapping a GraphNode's abstract status 
 * to the centralized semantic tokens defined in the UI Kit.
 */
export function resolveNodeColor(status: string) {
  // getStatusColors returns an object like: { bg, text, border, hex }
  return getStatusColors(status);
}
