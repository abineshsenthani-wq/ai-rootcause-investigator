import React, { useState } from 'react';
import { FileText, Download, Code, FileCode, CheckCircle, Sparkles } from 'lucide-react';
import { DatasetMeta } from '../types';
import { getReportDownloadUrl, runInvestigation } from '../services/api';

export const ReportsPage: React.FC<{ currentDataset: DatasetMeta | null }> = ({ currentDataset }) => {
  const [isExportingJson, setIsExportingJson] = useState(false);
  const [isExportingHtml, setIsExportingHtml] = useState(false);

  const handleDownloadPDF = () => {
    if (currentDataset?.id) {
      window.open(getReportDownloadUrl(currentDataset.id), '_blank');
    }
  };

  const handleExportJSON = async () => {
    if (!currentDataset?.id) return;
    setIsExportingJson(true);
    try {
      const data = await runInvestigation(currentDataset.id);
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `investigation_evidence_${currentDataset.id}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export JSON:', err);
    } finally {
      setIsExportingJson(false);
    }
  };

  const handleExportHTML = async () => {
    if (!currentDataset?.id) return;
    setIsExportingHtml(true);
    try {
      const data = await runInvestigation(currentDataset.id);
      const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Root-Cause Investigation Report - ${currentDataset.filename}</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; line-height: 1.6; }
        .container { max-width: 800px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 2rem; border: 1px solid #334155; }
        h1 { color: #818cf8; border-b: 1px solid #334155; padding-bottom: 0.5rem; }
        h2 { color: #38bdf8; margin-top: 1.5rem; }
        .badge { background: #312e81; color: #a5b4fc; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-family: monospace; }
        ul { padding-left: 1.2rem; }
        li { margin-bottom: 0.5rem; }
        .explanation { background: #090d16; padding: 1rem; border-radius: 8px; border-left: 4px solid #6366f1; white-space: pre-wrap; font-family: monospace; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Root-Cause Investigation Report</h1>
        <p><strong>Dataset:</strong> ${currentDataset.filename} <span class="badge">ID: ${currentDataset.id}</span></p>
        <p><strong>Metric Shift:</strong> ${data.event?.percentage_change}% (${data.event?.event_type})</p>
        <p><strong>Confidence:</strong> ${data.confidence}%</p>
        
        <h2>Executive Synthesis</h2>
        <div class="explanation">${data.ai_explanation || 'No summary available.'}</div>
        
        <h2>Verified Facts</h2>
        <ul>${(data.facts || []).map((f: string) => `<li>${f}</li>`).join('')}</ul>
        
        <h2>Recommendations</h2>
        <ul>${(data.recommendations || []).map((r: string) => `<li>${r}</li>`).join('')}</ul>
    </div>
</body>
</html>`;

      const blob = new Blob([htmlContent], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `investigation_report_${currentDataset.id}.html`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export HTML:', err);
    } finally {
      setIsExportingHtml(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-md">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-indigo-400" />
          Multi-Format Investigation Report Export Engine
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Export comprehensive evidence-grounded root-cause reports in printable PDF format, standalone HTML documents, or raw structured JSON payloads.
        </p>
      </div>

      {/* Export Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* PDF Export */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4 hover:border-indigo-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-3">
              <Download className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-semibold text-white">Printable PDF Report</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Formatted using ReportLab containing Executive Summary, Metric Change Breakdown, Anomalies, Evidence Scoring, and Recommendations.
            </p>
          </div>
          <button
            onClick={handleDownloadPDF}
            disabled={!currentDataset}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-lg transition-colors flex items-center justify-center gap-2 shadow-md disabled:opacity-50"
          >
            <Download className="w-4 h-4" /> Download PDF Report
          </button>
        </div>

        {/* HTML Export */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4 hover:border-sky-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 mb-3">
              <FileCode className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-semibold text-white">Standalone HTML Summary</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Export self-contained HTML executive report formatted for web distribution, browser printing, and email attachments.
            </p>
          </div>
          <button
            onClick={handleExportHTML}
            disabled={!currentDataset || isExportingHtml}
            className="w-full py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-medium text-xs rounded-lg transition-colors flex items-center justify-center gap-2 shadow-md disabled:opacity-50"
          >
            <FileCode className="w-4 h-4" /> {isExportingHtml ? 'Generating HTML...' : 'Export HTML Summary'}
          </button>
        </div>

        {/* JSON Export */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4 hover:border-emerald-500/40 transition-colors flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-3">
              <Code className="w-5 h-5" />
            </div>
            <h3 className="text-sm font-semibold text-white">Structured JSON Evidence</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Export raw machine-readable JSON payload containing statistical facts, segment contribution percentages, and correlation matrices.
            </p>
          </div>
          <button
            onClick={handleExportJSON}
            disabled={!currentDataset || isExportingJson}
            className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs rounded-lg transition-colors flex items-center justify-center gap-2 shadow-md disabled:opacity-50"
          >
            <Code className="w-4 h-4" /> {isExportingJson ? 'Exporting JSON...' : 'Export Raw JSON Data'}
          </button>
        </div>
      </div>
    </div>
  );
};
