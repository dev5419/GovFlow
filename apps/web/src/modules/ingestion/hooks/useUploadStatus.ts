import { useState, useEffect, useCallback } from 'react';
import { ProcessingJob } from '@govflow/shared-types';
import { ingestionApi } from '../api/ingestionApi';

export function useUploadStatus(jobId: string | null) {
  const [job, setJob] = useState<ProcessingJob | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const pollStatus = useCallback(async () => {
    if (!jobId) return;
    try {
      const data = await ingestionApi.getJobStatus(jobId);
      setJob(data);
      
      // Stop polling if the job is done or failed
      if (data.status === 'completed' || data.status === 'failed') {
        return true; // indicates done polling
      }
      return false; // keep polling
    } catch (err: any) {
      setError(err.message || 'Failed to fetch job status');
      return true; // Stop polling on hard error
    }
  }, [jobId]);

  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    
    const poll = async () => {
      const isDone = await pollStatus();
      if (!isDone) {
        timeoutId = setTimeout(poll, 2000); // poll every 2 seconds
      }
    };
    
    if (jobId) {
      poll();
    }
    
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [jobId, pollStatus]);

  return { job, error };
}
