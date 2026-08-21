import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, Activity } from 'lucide-react';
import { fetchMetricForecast } from '../services/api';

interface ForecastChartProps {
  datasetId: string;
  targetMetric: string;
}

export const ForecastChart: React.FC<ForecastChartProps> = ({ datasetId, targetMetric }) => {
  const [forecastData, setForecastData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!datasetId) return;
    setLoading(true);
    fetchMetricForecast(datasetId, targetMetric, 12)
      .then((data) => setForecastData(data))
      .catch((err) => console.error('Forecast fetch failed:', err))
      .finally(() => setLoading(false));
  }, [datasetId, targetMetric]);

  if (loading) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 h-64 flex items-center justify-center">
        <Activity className="w-6 h-6 text-indigo-400 animate-spin" />
      </div>
    );
  }

  const items = forecastData?.forecast || [];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            Time-Series Trend Projection (95% Confidence Band)
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Model: {forecastData?.model || 'ARIMA / Linear Trend'} | Slope: {forecastData?.slope} (r² = {forecastData?.r_squared})
          </p>
        </div>
        <span className="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-full">
          {forecastData?.trend_direction || 'Forecast'} Trend
        </span>
      </div>

      <div className="h-64 w-full pt-4">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={items} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="forecastBand" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="period" stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
            <YAxis stroke="#64748b" tick={{ fill: '#64748b', fontSize: 10 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
            />
            <Area type="monotone" dataKey="upper_bound_95" stroke="none" fill="url(#forecastBand)" name="Upper 95% CI" />
            <Area type="monotone" dataKey="projected_value" stroke="#10b981" strokeWidth={2} fill="none" name="Projected Metric" />
            <Area type="monotone" dataKey="lower_bound_95" stroke="none" fill="#0f172a" name="Lower 95% CI" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
