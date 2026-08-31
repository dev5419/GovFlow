import { ComplianceFlag, OfficerDecision } from "@govflow/shared-types";

// Mocking the base URL for now. In a real app, this would come from an env var.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const complianceApi = {
  /**
   * Fetch all compliance flags for a given bidder and tender.
   */
  getFlags: async (tenderId: string, bidderId: string): Promise<ComplianceFlag[]> => {
    const response = await fetch(`${API_BASE_URL}/tenders/${tenderId}/bidders/${bidderId}/flags`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        // In a real app, inject the JWT token here
        "Authorization": "Bearer MOCK_TOKEN"
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch compliance flags: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Record an officer's decision against a specific flag.
   */
  recordDecision: async (
    flagId: string, 
    decisionState: string, 
    notes?: string
  ): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/flags/${flagId}/decisions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer MOCK_TOKEN"
      },
      body: JSON.stringify({ decisionState, notes }),
    });

    if (!response.ok) {
      throw new Error(`Failed to record decision: ${response.statusText}`);
    }
  },
};
