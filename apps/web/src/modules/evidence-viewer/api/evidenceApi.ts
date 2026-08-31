import { ExtractedField, EvidenceAnchor } from "@govflow/shared-types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SignedUrlResponse {
  url: string;
  expires_at: number;
  document_id: string;
  page_number: number;
}

export interface EvidenceOverlayResponse {
  document_id: string;
  page_number: number;
  fields: ExtractedField[];
  anchors: EvidenceAnchor[];
}

export interface LinkedEvidenceResponse {
  source_anchor_id: string;
  linked_anchors: EvidenceAnchor[];
}

export const evidenceApi = {
  getSignedUrl: async (documentId: string, pageNumber: number) => {
    const response = await fetch(`${API_BASE_URL}/evidence/documents/${documentId}/pages/${pageNumber}/url`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    if (!response.ok) throw new Error("Failed to fetch signed URL");
    return response.json();
  },

  getOverlays: async (tenderId: string, bidderId: string, documentId: string, pageNumber: number): Promise<EvidenceOverlayResponse> => {
    const response = await fetch(`${API_BASE_URL}/evidence/overlays/tenders/${tenderId}/bidders/${bidderId}/documents/${documentId}/pages/${pageNumber}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    if (!response.ok) throw new Error("Failed to fetch evidence overlays");
    return response.json();
  },

  getLinkedEvidence: async (flagId: string, anchorId: string): Promise<LinkedEvidenceResponse> => {
    const response = await fetch(`${API_BASE_URL}/evidence/flags/${flagId}/anchors/${anchorId}/linked`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    if (!response.ok) throw new Error("Failed to fetch linked evidence");
    return response.json();
  }
};
