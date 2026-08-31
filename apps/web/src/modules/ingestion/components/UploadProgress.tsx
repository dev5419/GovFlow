import React from 'react';
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { ProcessingJob } from '@govflow/shared-types';

interface UploadProgressProps {
  fileName: string;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  error?: string | null;
}

export function UploadProgress({ fileName, progress, status, error }: UploadProgressProps) {
  const isComplete = status === 'completed';
  const isFailed = status === 'failed';
  const isInProgress = status === 'uploading' || status === 'processing';

  // Determine colors based on design specifications
  let fillBgColor = 'var(--color-primary)';
  if (isComplete) fillBgColor = 'var(--color-secondary)';
  if (isFailed) fillBgColor = 'var(--color-status-non-compliant)';

  let statusText = 'Processing...';
  if (status === 'uploading') statusText = 'Uploading...';
  if (isComplete) statusText = 'Complete';
  if (isFailed) statusText = 'Failed';

  return (
    <div className="flex flex-col gap-2 p-3 bg-white border border-[#DDE2E5] rounded-[4px]">
      <div className="flex justify-between items-center">
        <span className="text-[14px] font-semibold text-[#212529] truncate max-w-[70%]">
          {fileName}
        </span>
        <span 
          className="text-[12px] font-medium flex items-center gap-1"
          style={{ 
            color: isFailed ? 'var(--color-status-non-compliant)' : 
                   isComplete ? 'var(--color-secondary)' : 
                   'var(--color-text-secondary)'
          }}
          aria-live="polite"
        >
          {isInProgress && <Loader2 className="w-3 h-3 animate-spin" />}
          {isComplete && <CheckCircle className="w-3 h-3" />}
          {isFailed && <AlertCircle className="w-3 h-3" />}
          {statusText} {isInProgress && `${Math.round(progress)}%`}
        </span>
      </div>
      
      {/* Progress Bar Container */}
      <div 
        className="w-full h-2 rounded overflow-hidden relative"
        style={{ backgroundColor: 'var(--color-surface-alt)' }}
        role="progressbar"
        aria-valuenow={progress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Upload progress for ${fileName}`}
      >
        <div 
          className="h-full transition-all duration-300 ease-in-out"
          style={{ 
            width: `${progress}%`,
            backgroundColor: fillBgColor
          }}
        />
      </div>

      {isFailed && error && (
        <div className="text-[12px] text-[#DC2626] mt-1" role="alert" aria-live="assertive">
          {error}
        </div>
      )}
    </div>
  );
}
