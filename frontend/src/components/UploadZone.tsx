import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
import { uploadDataset } from '../services/api';
import { DatasetMeta } from '../types';

interface UploadZoneProps {
  onUploadSuccess: (dataset: DatasetMeta) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    const validExts = ['.csv', '.xlsx', '.xls'];
    const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();

    if (!validExts.includes(ext)) {
      setErrorMsg('Invalid file type. Please upload a CSV or Excel file (.csv, .xlsx, .xls).');
      return;
    }

    setErrorMsg(null);
    setIsUploading(true);

    try {
      const result = await uploadDataset(file);
      onUploadSuccess(result);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to upload dataset.');
    } finally {
      setIsUploading(false);
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="w-full">
      <div
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onDrop={onDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 ${
          isDragging
            ? 'border-indigo-500 bg-indigo-500/10'
            : 'border-slate-800 hover:border-slate-700 bg-slate-900/50 hover:bg-slate-900'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          className="hidden"
        />

        <div className="w-16 h-16 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 flex items-center justify-center mx-auto mb-4">
          <Upload className="w-8 h-8" />
        </div>

        <h3 className="text-base font-semibold text-white mb-1">
          Drop your CSV or Excel file here
        </h3>
        <p className="text-xs text-slate-400 font-mono mb-4">
          Supports CSV, XLSX, XLS up to 500 MB
        </p>

        {isUploading ? (
          <div className="flex items-center justify-center gap-2 text-xs font-mono text-indigo-400">
            <span className="w-4 h-4 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin"></span>
            Uploading and profiling dataset statistical properties...
          </div>
        ) : (
          <button
            type="button"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-medium transition-colors"
          >
            Browse Computer
          </button>
        )}
      </div>

      {errorMsg && (
        <div className="mt-4 p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center gap-2 text-xs text-rose-400">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}
    </div>
  );
};
