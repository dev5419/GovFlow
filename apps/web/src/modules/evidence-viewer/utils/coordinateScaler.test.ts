import { scaleCoordinates } from "./coordinateScaler";
import { BoundingBox } from "@govflow/shared-types";

describe("coordinateScaler", () => {
  it("scales coordinates correctly into CSS percentages", () => {
    const box: BoundingBox = {
      x0: 100,
      y0: 200,
      x1: 300,
      y1: 400,
      pageWidth: 1000,
      pageHeight: 2000
    };

    const scaled = scaleCoordinates(box);

    expect(scaled.left).toBe("10.0000%");
    expect(scaled.top).toBe("10.0000%");
    expect(scaled.width).toBe("20.0000%");
    expect(scaled.height).toBe("10.0000%");
  });

  it("handles missing pageWidth and pageHeight gracefully", () => {
    const box: BoundingBox = {
      x0: 100,
      y0: 200,
      x1: 300,
      y1: 400,
      pageWidth: 0,
      pageHeight: 0
    };

    const scaled = scaleCoordinates(box);

    expect(scaled.left).toBe("0%");
    expect(scaled.width).toBe("0%");
  });

  it("clamps coordinates to page dimensions", () => {
    const box: BoundingBox = {
      x0: -50,
      y0: -50,
      x1: 1500,
      y1: 2500,
      pageWidth: 1000,
      pageHeight: 2000
    };

    const scaled = scaleCoordinates(box);

    expect(scaled.left).toBe("0.0000%");
    expect(scaled.top).toBe("0.0000%");
    expect(scaled.width).toBe("100.0000%");
    expect(scaled.height).toBe("100.0000%");
  });
});
