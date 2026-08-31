import { GraphNode, GraphEdge } from "@govflow/shared-types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface BidderGraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export const graphApi = {
  getBidderGraph: async (tenderId: string, bidderId: string): Promise<BidderGraphResponse> => {
    const response = await fetch(`${API_BASE_URL}/graph/tenders/${tenderId}/bidders/${bidderId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      // In a real app, include JWT authorization here
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch bidder graph: ${response.statusText}`);
    }

    return response.json();
  }
};
