import React, { useEffect, useState } from 'react';
import { AlertTriangle, ShieldAlert, Search, Filter } from 'lucide-react';
import { DatasetMeta } from '../types';
import { fetchDatasetAnomalies } from '../services/api';
import { AnomalyChart } from '../components/AnomalyChart';

export const AnomaliesPage: React.FC<{ currentDataset: DatasetMeta | null }> = ({ currentDataset }) => {
  const [anomalyData, setAnomalyData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [selectedMethod, setSelectedMethod] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    if (currentDataset?.id) {
      setIsLoading(true);
      fetchDatasetAnomalies(currentDataset.id)
        .then(setAnomalyData)
        .catch(console.error)
        .finally(() => setIsLoading(false));
    }
  }, [currentDataset]);

  const summary = anomalyData?.summary_by_method || { IQR: 0, 'Z-Score': 0, 'Isolation Forest': 0 };

  const allAnomalies = anomalyData?.anomalies || [];
  const filteredAnomalies = allAnomalies.filter((a: any) => {
    const matchesSeverity = selectedSeverity === 'ALL' || (a.severity && a.severity.toUpperCase() === selectedSeverity);
    const matchesMethod = selectedMethod === 'ALL' || (a.method && a.method.toUpperCase().includes(selectedMethod));
    const matchesSearch = searchQuery === '' || 
      String(a.row_id).includes(searchQuery) || 
      String(a.metric).toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(a.value).includes(searchQuery);

    return matchesSeverity && matchesMethod && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header Panel */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-md">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          Multi-Method Anomaly Detection Engine
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Identifies statistical outliers across transactions using IQR, Z-Score standard deviation thresholds, and Isolation Forest ML models.
        </p>
      </div>

      {/* Summary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">IQR (Interquartile Range)</span>
          <span className="text-2xl font-bold text-amber-400 mt-2 block font-mono">{summary['IQR'] || 0} Outliers</span>
          <span className="text-xs text-slate-500 mt-1 block">Tukey 1.5x IQR boundary fence</span>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Z-Score (Standard Normal)</span>
          <span className="text-2xl font-bold text-amber-400 mt-2 block font-mono">{summary['Z-Score'] || 0} Outliers</span>
          <span className="text-xs text-slate-500 mt-1 block">|Z| &gt; 3.0 Standard Deviations</span>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Isolation Forest (ML)</span>
          <span className="text-2xl font-bold text-rose-400 mt-2 block font-mono">{summary['Isolation Forest'] || 0} Outliers</span>
          <span className="text-xs text-slate-500 mt-1 block">Unsupervised decision trees (Contamination 0.01)</span>
        </div>
      </div>

      {/* Visual Anomaly Scatter Plot */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-indigo-400" /> Visual Outlier Score Distribution
        </h3>
        <AnomalyChart anomalies={filteredAnomalies} />
      </div>

      {/* Filterable Anomalies Table */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              Detected Transaction Outliers
            </h3>
            <span className="text-xs text-slate-500 font-mono">
              Showing {filteredAnomalies.length} of {allAnomalies.length} total detected anomalies
            </span>
          </div>

          {/* Interactive Filter Bar */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <div className="flex items-center gap-1.5 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
              <Search className="w-3.5 h-3.5 text-slate-500" />
              <input
                type="text"
                placeholder="Search row or metric..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-transparent text-slate-200 focus:outline-none text-xs font-mono w-36"
              />
            </div>

            <div className="flex items-center gap-1 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
              <Filter className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-slate-400">Severity:</span>
              <select
                value={selectedSeverity}
                onChange={(e) => setSelectedSeverity(e.target.value)}
                className="bg-transparent text-slate-200 font-mono focus:outline-none text-xs"
              >
                <option value="ALL" className="bg-slate-900">All</option>
                <option value="CRITICAL" className="bg-slate-900">Critical</option>
                <option value="HIGH" className="bg-slate-900">High</option>
                <option value="MEDIUM" className="bg-slate-900">Medium</option>
                <option value="LOW" className="bg-slate-900">Low</option>
              </select>
            </div>

            <div className="flex items-center gap-1 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
              <span className="text-slate-400">Method:</span>
              <select
                value={selectedMethod}
                onChange={(e) => setSelectedMethod(e.target.value)}
                className="bg-transparent text-slate-200 font-mono focus:outline-none text-xs"
              >
                <option value="ALL" className="bg-slate-900">All Methods</option>
                <option value="IQR" className="bg-slate-900">IQR</option>
                <option value="Z-SCORE" className="bg-slate-900">Z-Score</option>
                <option value="ISOLATION" className="bg-slate-900">Isolation Forest</option>
              </select>
            </div>
          </div>
        </div>

        {isLoading ? (
          <div className="h-48 flex items-center justify-center text-slate-500 text-xs font-mono">
            Running multi-method anomaly detection algorithms...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                <tr>
                  <th className="p-3">Row Index</th>
                  <th className="p-3">Target Metric</th>
                  <th className="p-3">Value</th>
                  <th className="p-3">Expected Boundary Range</th>
                  <th className="p-3">Method</th>
                  <th className="p-3">Severity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-850">
                {filteredAnomalies.length > 0 ? (
                  filteredAnomalies.slice(0, 30).map((a: any, idx: number) => (
                    <tr key={idx} className="hover:bg-slate-850/50 transition-colors">
                      <td className="p-3 text-slate-400">#{a.row_id}</td>
                      <td className="p-3 text-indigo-400 font-semibold">{a.metric}</td>
                      <td className="p-3 text-white font-bold">{a.value?.toLocaleString()}</td>
                      <td className="p-3 text-slate-400">{a.expected_range}</td>
                      <td className="p-3 text-slate-300">{a.method}</td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          a.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40' :
                          a.severity === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40' : 'bg-slate-800 text-slate-300'
                        }`}>
                          {a.severity}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="p-6 text-center text-slate-500 font-mono">
                      No matching anomalies found for selected filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
