'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { UploadDropzone } from '../../../../modules/ingestion/components/UploadDropzone';
import { ProcessingStatus } from '../../../../modules/ingestion/components/ProcessingStatus';
import { ingestionApi } from '../../../../modules/ingestion/api/ingestionApi';

interface UploadItem {
  id: string; // temporary unique id for UI tracking before we get jobId
  file: File;
  jobId?: string;
  error?: string;
}

export default function DocumentUploadPage() {
  const params = useParams();
  const tenderId = params.tenderId as string;
  
  const [uploads, setUploads] = useState<UploadItem[]>([]);

  const handleFilesAccepted = async (files: File[]) => {
    // Add files to UI state immediately
    const newUploads = files.map(file => ({
      id: Math.random().toString(36).substring(2, 9),
      file
    }));
    
    setUploads(prev => [...newUploads, ...prev]);

    // Start upload process for each file
    newUploads.forEach(async (uploadItem) => {
      try {
        const res = await ingestionApi.uploadDocument(tenderId, uploadItem.file);
        
        setUploads(prev => prev.map(u => {
          if (u.id === uploadItem.id) {
            return { ...u, jobId: res.job_id };
          }
          return u;
        }));
      } catch (err: any) {
        setUploads(prev => prev.map(u => {
          if (u.id === uploadItem.id) {
            return { ...u, error: err.message || 'Upload failed due to a server error.' };
          }
          return u;
        }));
      }
    });
  };

  return (
    <div className="gov-container py-8 flex flex-col gap-8">
      <div>
        <h1 className="mb-2">Document Ingestion</h1>
        <p className="text-[14px] text-[var(--color-text-secondary)]">
          Upload documents for tender <strong>{tenderId}</strong>. Documents will be queued for text extraction and compliance evaluation.
        </p>
      </div>

      <section className="flex flex-col lg:flex-row gap-8 items-start">
        <div className="w-full lg:w-2/3 flex flex-col gap-4">
          <div className="gov-card p-6">
            <h2 className="text-[18px] mb-4">Upload New Documents</h2>
            <UploadDropzone onFilesAccepted={handleFilesAccepted} maxSizeMB={50} />
          </div>
        </div>
        
        <div className="w-full lg:w-1/3 flex flex-col gap-4">
          <div className="gov-card p-6 flex flex-col gap-4">
            <h2 className="text-[18px] border-b border-[var(--color-border)] pb-2 mb-2">Processing Status</h2>
            
            {uploads.length === 0 ? (
              <p className="text-[14px] text-[var(--color-text-secondary)]">
                No active uploads.
              </p>
            ) : (
              <div className="flex flex-col gap-3 max-h-[600px] overflow-y-auto pr-2">
                {uploads.map(upload => (
                  upload.jobId ? (
                    <ProcessingStatus 
                      key={upload.id} 
                      jobId={upload.jobId} 
                      fileName={upload.file.name} 
                    />
                  ) : (
                    // Display a mock UploadProgress while the actual file upload POST is pending
                    <div key={upload.id} className="flex flex-col gap-2 p-3 bg-white border border-[#DDE2E5] rounded-[4px]">
                      <div className="flex justify-between items-center">
                        <span className="text-[14px] font-semibold text-[#212529] truncate max-w-[70%]">
                          {upload.file.name}
                        </span>
                        <span className="text-[12px] font-medium" style={{ color: upload.error ? 'var(--color-status-non-compliant)' : 'var(--color-text-secondary)' }}>
                          {upload.error ? 'Failed' : 'Uploading...'}
                        </span>
                      </div>
                      <div className="w-full h-2 rounded overflow-hidden relative" style={{ backgroundColor: 'var(--color-surface-alt)' }}>
                        {!upload.error && (
                          <div 
                            className="h-full transition-all duration-300 ease-in-out w-1/4 animate-pulse"
                            style={{ backgroundColor: 'var(--color-primary)' }}
                          />
                        )}
                      </div>
                      {upload.error && (
                        <div className="text-[12px] text-[#DC2626] mt-1">
                          {upload.error}
                        </div>
                      )}
                    </div>
                  )
                ))}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}