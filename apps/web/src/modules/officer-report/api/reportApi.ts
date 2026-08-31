const API_BASE_URL = process.env.NEXT_PUBLIC_API_GATEWAY_URL || "http://localhost:8000";

export interface ReportData {
  id: string;
  tender_id: string;
  bidder_id: string;
  status: "PENDING" | "COMPLETED" | "FAILED";
  requested_by: string;
  created_at: string;
  updated_at: string;
  download_url?: string;
}

export const reportApi = {
  async getReports(tenderId: string, bidderId: string): Promise<ReportData[]> {
    // Hardcoded token for Procurement Officer role as per earlier implementations
    const token = "procurement_officer_token"; 
    
    const response = await fetch(`${API_BASE_URL}/tenders/${tenderId}/bidders/${bidderId}/reports`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch reports: ${response.statusText}`);
    }

    return response.json();
  },

  async generateReport(tenderId: string, bidderId: string): Promise<ReportData> {
    const token = "procurement_officer_token"; 
    
    const response = await fetch(`${API_BASE_URL}/tenders/${tenderId}/bidders/${bidderId}/reports`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to trigger report generation: ${response.statusText}`);
    }

    return response.json();
  }
};
