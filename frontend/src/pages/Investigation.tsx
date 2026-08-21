import React, { useState, useEffect } from 'react';
import { Search, Play, ShieldAlert, Download, FileText } from 'lucide-react';
import { DatasetMeta } from '../types';
import { runInvestigation, getReportDownloadUrl, fetchDatasetProfile } from '../services/api';
import { InvestigationPanel } from '../components/InvestigationPanel';

export const InvestigationPage: React.FC<{ currentDataset: DatasetMeta | null }> = ({ currentDataset }) => {
  const [selectedMetric, setSelectedMetric] = useState<string>('');
  const [availableMetrics, setAvailableMetrics] = useState<string[]>([]);
  const [timePeriod, setTimePeriod] = useState<string>('Auto-Detected Period Shift');
  const [question, setQuestion] = useState<string>('Why did the metric change?');
  const [isInvestigating, setIsInvestigating] = useState<boolean>(false);
  const [investigationData, setInvestigationData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentDataset?.id) {
      setInvestigationData(null);
      setError(null);
      if (currentDataset.primary_metric) {
        setSelectedMetric(currentDataset.primary_metric);
        setAvailableMetrics([currentDataset.primary_metric]);
      }

      fetchDatasetProfile(currentDataset.id)
        .then((profile) => {
          const numCols = profile.classification?.numerical_columns || [];
          if (numCols.length > 0) {
            setAvailableMetrics(numCols);
            setSelectedMetric(currentDataset.primary_metric || numCols[0]);
          }
        })
        .catch(console.error);
    } else {
      setInvestigationData(null);
    }
  }, [currentDataset?.id]);

  const handleRunInvestigation = async () => {
    if (!currentDataset?.id) {
      setError('Please select or upload a dataset first.');
      return;
    }
    setIsInvestigating(true);
    setError(null);

    try {
      const data = await runInvestigation(currentDataset.id, {
        metric: selectedMetric || currentDataset.primary_metric,
        question: question
      });
      setInvestigationData(data);
    } catch (err: any) {
      setError(err.message || 'Investigation failed');
    } finally {
      setIsInvestigating(false);
    }
  };

  const handleDownloadPDF = () => {
    if (currentDataset?.id) {
      window.open(getReportDownloadUrl(currentDataset.id), '_blank');
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Query Control Console */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-xl">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
          <Search className="w-5 h-5 text-indigo-400" />
          Automated Multi-Agent Root-Cause Investigation Console
        </h2>

        {error && (
          <div className="mb-4 p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 text-xs font-mono">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 text-xs">
          <div>
            <label className="text-slate-400 block mb-1 font-medium">Target Metric</label>
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500 font-medium capitalize"
            >
              {availableMetrics.length > 0 ? (
                availableMetrics.map((m) => (
                  <option key={m} value={m}>
                    {m.replace('_', ' ').toUpperCase()}
                  </option>
                ))
              ) : (
                <option value={currentDataset?.primary_metric || 'revenue'}>
                  {(currentDataset?.primary_metric || 'revenue').toUpperCase()}
                </option>
              )}
            </select>
          </div>

          <div>
            <label className="text-slate-400 block mb-1 font-medium">Comparison Period</label>
            <input
              type="text"
              value={timePeriod}
              onChange={(e) => setTimePeriod(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500 font-medium"
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1 font-medium">Investigation Question</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-indigo-500 font-medium"
              placeholder="e.g. Why did the metric change?"
            />
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3">
          <button
            onClick={handleRunInvestigation}
            disabled={isInvestigating}
            className="w-full sm:w-auto px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-lg transition-colors shadow-md flex items-center justify-center gap-2"
          >
            {isInvestigating ? (
              <>
                <span className="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
                Executing Multi-Agent Causal & Vector Pipeline...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                Run Full Multi-Agent Investigation
              </>
            )}
          </button>

          {investigationData && (
            <button
              onClick={handleDownloadPDF}
              className="w-full sm:w-auto px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium text-xs rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              <Download className="w-4 h-4 text-indigo-400" />
              Download PDF Report
            </button>
          )}
        </div>
      </div>

      {/* Dynamic Results View */}
      {investigationData && (
        <InvestigationPanel investigation={investigationData} datasetId={currentDataset?.id} />
      )}
    </div>
  );
};
