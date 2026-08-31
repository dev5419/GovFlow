import { BoundingBox } from "@govflow/shared-types";

export interface ScaledBox {
  left: string;
  top: string;
  width: string;
  height: string;
}

/**
 * Calculates CSS percentage values for absolute positioning a bounding box
 * overlay on top of a rendered document canvas.
 * 
 * We use percentages rather than absolute pixels so that if the window
 * is resized natively by the browser, the boxes scale fluidly.
 * 
 * @param box The original BoundingBox from the API
 * @param renderedWidth The actual pixel width of the DOM canvas wrapper
 * @param renderedHeight The actual pixel height of the DOM canvas wrapper
 */
export function scaleCoordinates(box: BoundingBox): ScaledBox {
  if (!box.pageWidth || !box.pageHeight) {
    console.warn("BoundingBox missing pageWidth or pageHeight. Falling back to 0.");
    return { left: "0%", top: "0%", width: "0%", height: "0%" };
  }

  // Ensure bounds don't exceed page bounds
  const x0 = Math.max(0, box.x0);
  const y0 = Math.max(0, box.y0);
  const x1 = Math.min(box.pageWidth, box.x1);
  const y1 = Math.min(box.pageHeight, box.y1);

  const leftPct = (x0 / box.pageWidth) * 100;
  const topPct = (y0 / box.pageHeight) * 100;
  const widthPct = ((x1 - x0) / box.pageWidth) * 100;
  const heightPct = ((y1 - y0) / box.pageHeight) * 100;

  return {
    left: `${leftPct.toFixed(4)}%`,
    top: `${topPct.toFixed(4)}%`,
    width: `${widthPct.toFixed(4)}%`,
    height: `${heightPct.toFixed(4)}%`
  };
}
