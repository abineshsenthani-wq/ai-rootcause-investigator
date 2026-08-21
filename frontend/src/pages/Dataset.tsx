import React, { useState, useEffect } from 'react';
import { Upload, FileSpreadsheet, CheckCircle2, Database, AlertCircle, Table, ShieldCheck, Sparkles } from 'lucide-react';
import { DatasetMeta } from '../types';
import { uploadDataset, fetchDatasetProfile } from '../services/api';

interface DatasetPageProps {
  currentDataset: DatasetMeta | null;
  datasetsList?: DatasetMeta[];
  onSelectDataset?: (meta: DatasetMeta) => void;
  onDatasetUploaded: (meta: DatasetMeta) => void;
}

export const DatasetPage: React.FC<DatasetPageProps> = ({
  currentDataset,
  datasetsList = [],
  onSelectDataset,
  onDatasetUploaded
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [profileData, setProfileData] = useState<any | null>(null);
  const [isLoadingProfile, setIsLoadingProfile] = useState<boolean>(false);

  useEffect(() => {
    if (currentDataset?.id) {
      setIsLoadingProfile(true);
      fetchDatasetProfile(currentDataset.id)
        .then(setProfileData)
        .catch(console.error)
        .finally(() => setIsLoadingProfile(false));
    }
  }, [currentDataset?.id]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);
    setSuccessMsg(null);

    try {
      const uploadedMeta = await uploadDataset(file);
      onDatasetUploaded(uploadedMeta);
      setSuccessMsg(`Successfully uploaded and profiled '${uploadedMeta.filename}' (${uploadedMeta.row_count.toLocaleString()} rows).`);
    } catch (err: any) {
      setError(err.message || 'Error uploading dataset');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Zone Panel */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-md">
        <h2 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
          <Database className="w-5 h-5 text-indigo-400" />
          Dataset Ingestion & File Storage
        </h2>
        <p className="text-slate-400 text-sm">
          Upload your business dataset (CSV or Excel) containing transactions, dates, numerical metrics, and breakdown dimensions.
        </p>

        {error && (
          <div className="mt-4 p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            {error}
          </div>
        )}

        {successMsg && (
          <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            {successMsg}
          </div>
        )}

        <div className="mt-6 border-2 border-dashed border-slate-800 hover:border-indigo-500/50 transition-colors rounded-xl p-8 flex flex-col items-center justify-center bg-slate-950/40 text-center">
          <FileSpreadsheet className="w-12 h-12 text-indigo-400/80 mb-3 animate-bounce" />
          <h3 className="text-sm font-medium text-slate-200">Drag & Drop Business Dataset</h3>
          <p className="text-xs text-slate-500 mt-1">Supports CSV, XLSX up to 500 MB (1,000,000+ rows supported)</p>

          <label className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-lg cursor-pointer transition-colors shadow-md flex items-center gap-2">
            <Upload className="w-4 h-4" />
            {isUploading ? 'Uploading & Profiling...' : 'Select CSV/XLSX File'}
            <input type="file" accept=".csv, .xlsx, .xls" onChange={handleFileUpload} className="hidden" />
          </label>
        </div>
      </div>

      {/* Uploaded Datasets Repository List */}
      {datasetsList.length > 0 && (
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-indigo-400" /> Uploaded Datasets ({datasetsList.length})
            </h3>
            <span className="text-xs text-slate-500 font-mono">Select a dataset to activate for analysis</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {datasetsList.map((ds) => {
              const isSelected = currentDataset?.id === ds.id;
              return (
                <div
                  key={ds.id}
                  onClick={() => onSelectDataset && onSelectDataset(ds)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all flex items-center justify-between gap-3 ${
                    isSelected
                      ? 'bg-indigo-600/15 border-indigo-500/50 shadow-md'
                      : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <FileSpreadsheet className={`w-4 h-4 ${isSelected ? 'text-indigo-400' : 'text-slate-400'}`} />
                      <span className="font-semibold text-xs text-white truncate font-mono">{ds.filename}</span>
                    </div>
                    <div className="text-[11px] text-slate-400 mt-1 font-mono flex items-center gap-3">
                      <span>{ds.row_count.toLocaleString()} rows</span>
                      <span>•</span>
                      <span className="text-indigo-300 uppercase">{ds.primary_metric}</span>
                    </div>
                  </div>

                  {isSelected ? (
                    <span className="px-2.5 py-1 bg-indigo-600 text-white rounded text-[10px] font-bold uppercase tracking-wider flex-shrink-0">
                      Active
                    </span>
                  ) : (
                    <button
                      type="button"
                      className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-medium transition-colors flex-shrink-0"
                    >
                      Select
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Active Dataset Metadata Summary */}
      {currentDataset && (
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Active Ingested Dataset Metadata
            </h3>
            <span className="text-xs text-slate-500 font-mono">ID: {currentDataset.id}</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-850">
              <span className="text-slate-500 block">Filename</span>
              <span className="font-semibold text-slate-200 font-mono mt-1 block truncate">{currentDataset.filename}</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-850">
              <span className="text-slate-500 block">Row Count</span>
              <span className="font-semibold text-slate-200 mt-1 block font-mono">{currentDataset.row_count.toLocaleString()}</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-850">
              <span className="text-slate-500 block">Primary Metric</span>
              <span className="font-semibold text-indigo-400 mt-1 block uppercase font-mono">{currentDataset.primary_metric || 'revenue'}</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-850">
              <span className="text-slate-500 block">Date Range</span>
              <span className="font-semibold text-slate-200 mt-1 block font-mono">{currentDataset.date_min || '2026-01-01'} → {currentDataset.date_max || '2026-07-31'}</span>
            </div>
          </div>
        </div>
      )}

      {/* Column-by-Column Statistical Profiling Table */}
      {currentDataset && (
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Table className="w-4 h-4 text-indigo-400" /> Statistical Profiling & Data Quality Audit
            </h3>
            {profileData?.quality_assessment && (
              <span className="text-xs px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full font-mono font-bold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" /> Quality Score: {profileData.quality_assessment.completeness_score}%
              </span>
            )}
          </div>

          {isLoadingProfile ? (
            <div className="py-8 text-center text-xs font-mono text-slate-500 flex items-center justify-center gap-2">
              <span className="w-4 h-4 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin"></span>
              Computing statistical column distributions and quality assessment...
            </div>
          ) : profileData?.column_profiles ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] bg-slate-950/60">
                    <th className="p-3">Column</th>
                    <th className="p-3">Inferred Type</th>
                    <th className="p-3">Missing %</th>
                    <th className="p-3">Unique Values</th>
                    <th className="p-3">Mean / Mode</th>
                    <th className="p-3">Min → Max</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-850 text-slate-300">
                  {Object.entries(profileData.column_profiles).map(([colName, stats]: [string, any]) => (
                    <tr key={colName} className="hover:bg-slate-850/50 transition-colors">
                      <td className="p-3 font-semibold text-white">{colName}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 rounded text-[10px] uppercase font-bold">
                          {stats.type}
                        </span>
                      </td>
                      <td className="p-3">
                        <span className={stats.missing_pct > 0 ? 'text-amber-400' : 'text-emerald-400'}>
                          {stats.missing_pct.toFixed(1)}% ({stats.missing_count})
                        </span>
                      </td>
                      <td className="p-3">{stats.unique_values?.toLocaleString()}</td>
                      <td className="p-3 font-sans">
                        {stats.mean !== undefined ? stats.mean.toLocaleString() : (stats.top_value || 'N/A')}
                      </td>
                      <td className="p-3 font-sans text-slate-400">
                        {stats.min !== undefined ? `${stats.min.toLocaleString()} → ${stats.max.toLocaleString()}` : 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-xs font-mono text-slate-500">No column profiles generated yet.</p>
          )}
        </div>
      )}
    </div>
  );
};
