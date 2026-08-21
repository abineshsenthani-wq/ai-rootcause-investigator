import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';

interface TrendChartProps {
  data: any[];
  dateKey?: string;
  valueKey?: string;
  height?: number;
}

export const TrendChart: React.FC<TrendChartProps> = ({
  data,
  dateKey = 'order_date',
  valueKey = 'revenue',
  height = 240
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center bg-slate-950/40 rounded-lg border border-dashed border-slate-800 text-slate-500 text-xs">
        No time-series data available for chart.
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="metricGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey={dateKey} stroke="#64748b" fontSize={11} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            itemStyle={{ color: '#818cf8' }}
          />
          <Area type="monotone" dataKey={valueKey} stroke="#6366f1" strokeWidth={2} fillOpacity={1} fill="url(#metricGradient)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
