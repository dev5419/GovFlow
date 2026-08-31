import { ProcessingJob } from '@govflow/shared-types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DocumentUploadResponse {
  job_id: string;
  document_id: string;
  status: string;
}

export const ingestionApi = {
  uploadDocument: async (tenderId: string, file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/tenders/${tenderId}/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Upload failed with status ${response.status}`);
    }
    
    return response.json();
  },
  
  getJobStatus: async (jobId: string): Promise<ProcessingJob> => {
    const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
      method: 'GET',
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Failed to get job status with status ${response.status}`);
    }
    
    return response.json();
  }
};
