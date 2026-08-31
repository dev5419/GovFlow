import React from 'react';
import { useUploadStatus } from '../hooks/useUploadStatus';
import { UploadProgress } from './UploadProgress';

interface ProcessingStatusProps {
  jobId: string;
  fileName: string;
}

export function ProcessingStatus({ jobId, fileName }: ProcessingStatusProps) {
  const { job, error } = useUploadStatus(jobId);

  // Map backend processing job status to our UI status
  let status: 'uploading' | 'processing' | 'completed' | 'failed' = 'processing';
  let progress = 0;

  if (job) {
    if (job.status === 'completed') {
      status = 'completed';
      progress = 100;
    } else if (job.status === 'failed') {
      status = 'failed';
      progress = job.progress || 0;
    } else {
      status = 'processing';
      progress = job.progress || 10; // show some minimal progress if queued/processing
    }
  } else if (error) {
    status = 'failed';
  } else {
    // If we haven't loaded the job yet, consider it processing
    status = 'processing';
    progress = 5;
  }

  return (
    <UploadProgress 
      fileName={fileName}
      progress={progress}
      status={status}
      error={error || job?.error_message}
    />
  );
}
