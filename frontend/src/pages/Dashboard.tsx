import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, TrendingDown, Layers, FileSpreadsheet, Play, Clock } from 'lucide-react';
import { DatasetMeta } from '../types';
import { fetchDatasetTrends, fetchDatasetAnomalies } from '../services/api';
import { TrendChart } from '../components/Charts/TrendChart';

interface DashboardProps {
  currentDataset: DatasetMeta | null;
  onNavigate: (tab: any) => void;
}

export const DashboardPage: React.FC<DashboardProps> = ({ currentDataset, onNavigate }) => {
  const [trends, setTrends] = useState<any[]>([]);
  const [anomalyCount, setAnomalyCount] = useState<number>(0);
  const [metricChange, setMetricChange] = useState<number>(0);
  const [granularity, setGranularity] = useState<string>('M');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    if (currentDataset?.id) {
      setIsLoading(true);
      fetchDatasetTrends(currentDataset.id, currentDataset.primary_metric, granularity)
        .then((res) => {
          if (res.trend_points) setTrends(res.trend_points);
          if (res.summary?.percentage_change !== undefined) setMetricChange(res.summary.percentage_change);
        })
        .catch(console.error);

      fetchDatasetAnomalies(currentDataset.id)
        .then((res) => {
          if (res.total_anomalies !== undefined) setAnomalyCount(res.total_anomalies);
        })
        .catch(console.error)
        .finally(() => setIsLoading(false));
    }
  }, [currentDataset, granularity]);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-850 to-indigo-950/60 p-6 rounded-xl border border-slate-800 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-indigo-400" />
            AI Root-Cause Investigator Overview
          </h2>
          <p className="text-slate-400 text-sm mt-1">
            Automated anomaly detection, metric shift investigation, and evidence-backed root-cause analysis.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => onNavigate('investigation')}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-lg transition-colors flex items-center gap-2 shadow-md"
          >
            <Play className="w-4 h-4 fill-current" />
            Start Investigation
          </button>
          <button
            onClick={() => onNavigate('datasets')}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium text-xs rounded-lg transition-colors flex items-center gap-2 shadow-md"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Manage Datasets
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 hover:border-slate-700 transition-all">
          <div className="flex justify-between items-center text-slate-400 text-xs font-medium uppercase tracking-wider">
            Primary Metric
            <TrendingDown className="w-4 h-4 text-rose-400" />
          </div>
          <div className="mt-3 text-2xl font-bold text-white capitalize truncate">
            {currentDataset?.primary_metric || 'Revenue'}
          </div>
          <div className="mt-1 text-xs text-rose-400 flex items-center gap-1 font-mono">
            <span>{metricChange > 0 ? `+${metricChange.toFixed(1)}%` : `${metricChange.toFixed(1)}%`}</span> vs Previous Window
          </div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 hover:border-slate-700 transition-all">
          <div className="flex justify-between items-center text-slate-400 text-xs font-medium uppercase tracking-wider">
            Total Dataset Rows
            <Layers className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="mt-3 text-2xl font-bold text-white font-mono">
            {currentDataset?.row_count?.toLocaleString() || '0'}
          </div>
          <div className="mt-1 text-xs text-slate-500">
            {currentDataset?.column_count || 0} Analytical Attributes
          </div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 hover:border-slate-700 transition-all">
          <div className="flex justify-between items-center text-slate-400 text-xs font-medium uppercase tracking-wider">
            Detected Outliers
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-3 text-2xl font-bold text-amber-400 font-mono">
            {anomalyCount}
          </div>
          <div className="mt-1 text-xs text-amber-500/80">
            IQR, Z-Score & Isolation Forest
          </div>
        </div>

        <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 hover:border-slate-700 transition-all">
          <div className="flex justify-between items-center text-slate-400 text-xs font-medium uppercase tracking-wider">
            Investigation Status
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          </div>
          <div className="mt-3 text-sm font-bold text-emerald-400 flex items-center gap-1.5 font-mono">
            Analysis Ready
          </div>
          <div className="mt-1 text-xs text-slate-400">
            Click Investigation tab to run analysis
          </div>
        </div>
      </div>

      {/* Main Dashboard Time Series Canvas with Granularity Selector */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 capitalize">
              {currentDataset?.primary_metric || 'Revenue'} Time Series Trend
            </h3>
            <span className="text-xs text-slate-500 font-mono">Resampled Time Series Plot</span>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-850 text-xs font-mono">
            <Clock className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-slate-400">Granularity:</span>
            <select
              value={granularity}
              onChange={(e) => setGranularity(e.target.value)}
              className="bg-transparent text-slate-200 font-bold focus:outline-none text-xs"
            >
              <option value="D" className="bg-slate-900">Daily (D)</option>
              <option value="W" className="bg-slate-900">Weekly (W)</option>
              <option value="M" className="bg-slate-900">Monthly (M)</option>
              <option value="Q" className="bg-slate-900">Quarterly (Q)</option>
            </select>
          </div>
        </div>

        {isLoading ? (
          <div className="h-64 flex items-center justify-center text-slate-500 text-xs font-mono">
            Loading metric time-series trends ({granularity})...
          </div>
        ) : (
          <TrendChart data={trends} valueKey={currentDataset?.primary_metric || 'revenue'} />
        )}
      </div>
    </div>
  );
};
