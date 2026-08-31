const API_BASE_URL = process.env.NEXT_PUBLIC_API_GATEWAY_URL || "http://localhost:8000";

export interface AuditEvent {
  id: string;
  tender_id: string;
  bidder_id: string;
  document_id?: string;
  flag_id?: string;
  officer_user_id: string;
  previous_state: string;
  new_state: string;
  action_type: string;
  notes?: string;
  created_at: string;
}

export const auditApi = {
  async getBidderAuditTrail(bidderId: string): Promise<AuditEvent[]> {
    const token = "procurement_officer_token"; // Mock token
    
    const response = await fetch(`${API_BASE_URL}/audit/bidders/${bidderId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch audit trail: ${response.statusText}`);
    }

    return response.json();
  }
};
