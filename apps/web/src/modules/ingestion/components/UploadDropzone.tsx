import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { Upload, AlertCircle } from 'lucide-react';

export interface FileValidationError {
  file: File;
  error: string;
}

interface UploadDropzoneProps {
  onFilesAccepted: (files: File[]) => void;
  maxSizeMB?: number;
}

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.zip'];
const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'image/png',
  'image/jpeg',
  'application/zip',
  'application/x-zip-compressed'
];

export function UploadDropzone({ onFilesAccepted, maxSizeMB = 50 }: UploadDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [validationErrors, setValidationErrors] = useState<FileValidationError[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFiles = (files: File[]): File[] => {
    const valid: File[] = [];
    const invalid: FileValidationError[] = [];

    files.forEach(file => {
      const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
      if (!ALLOWED_EXTENSIONS.includes(extension) && !ALLOWED_MIME_TYPES.includes(file.type)) {
        invalid.push({
          file,
          error: 'File type not supported. Upload .pdf, .png, .jpg, or .zip only.'
        });
        return;
      }

      if (file.size > maxSizeMB * 1024 * 1024) {
        invalid.push({
          file,
          error: `File size exceeds the ${maxSizeMB}MB limit.`
        });
        return;
      }

      valid.push(file);
    });

    setValidationErrors(invalid);
    return valid;
  };

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragActive) {
      setIsDragActive(true);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const filesArray = Array.from(e.dataTransfer.files);
      const validFiles = validateFiles(filesArray);
      if (validFiles.length > 0) {
        onFilesAccepted(validFiles);
      }
      e.dataTransfer.clearData();
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const filesArray = Array.from(e.target.files);
      const validFiles = validateFiles(filesArray);
      if (validFiles.length > 0) {
        onFilesAccepted(validFiles);
      }
      // Reset input value to allow selecting the same file again if needed
      e.target.value = '';
    }
  };

  const openFileDialog = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  let borderColorClass = 'border-[#C4CDD5]';
  if (isDragActive) {
    borderColorClass = 'border-[var(--color-accent)]';
  } else if (validationErrors.length > 0) {
    borderColorClass = 'border-[var(--color-status-non-compliant)]';
  }

  return (
    <div className="flex flex-col gap-4">
      <div
        className={`gov-card border-dashed ${borderColorClass} border-2 flex flex-col items-center justify-center py-12 px-6 text-center cursor-pointer transition-colors duration-200 bg-[var(--color-bg-base)]`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={openFileDialog}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openFileDialog();
          }
        }}
        aria-label="Upload document dropzone"
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleChange}
          className="hidden"
          multiple
          accept=".pdf,.png,.jpg,.jpeg,.zip,application/pdf,image/png,image/jpeg,application/zip"
          aria-hidden="true"
        />
        <div className="w-12 h-12 rounded-full bg-white flex items-center justify-center border border-[#DDE2E5] mb-4 shadow-sm">
          <Upload className="w-6 h-6 text-[var(--color-primary)]" />
        </div>
        <h3 className="text-[18px] font-semibold text-[var(--color-primary)] mb-2">
          Select files to upload
        </h3>
        <p className="text-[14px] text-[var(--color-text-secondary)] max-w-[400px]">
          Drag and drop files here, or click to browse.
          <br />
          Supported formats: .pdf, .png, .jpg, .zip (Max {maxSizeMB}MB)
        </p>
      </div>

      {validationErrors.length > 0 && (
        <div 
          className="flex flex-col gap-2 p-4 bg-[var(--color-status-non-compliant-bg)] border border-[var(--color-status-non-compliant)] rounded-[4px]"
          role="alert" 
          aria-live="assertive"
        >
          <div className="flex items-center gap-2 text-[var(--color-status-non-compliant)] font-semibold text-[14px]">
            <AlertCircle className="w-4 h-4" />
            <span>Validation Errors</span>
          </div>
          <ul className="list-disc pl-6 text-[14px] text-[var(--color-text-primary)]">
            {validationErrors.map((err, index) => (
              <li key={index}>
                <strong>{err.file.name}:</strong> {err.error}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
