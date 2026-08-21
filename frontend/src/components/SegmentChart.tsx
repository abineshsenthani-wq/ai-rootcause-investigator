import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface SegmentChartProps {
  factors: any[];
}

export const SegmentChart: React.FC<SegmentChartProps> = ({ factors }) => {
  if (!factors || factors.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-xs text-slate-500 font-mono">
        No segment breakdown factors isolated.
      </div>
    );
  }

  const chartData = factors.map((item) => ({
    name: `${item.dimension}: ${item.segment}`,
    changePct: item.metric_change_pct,
    contributionPct: item.contribution_pct,
    score: item.evidence_score
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 10, right: 10, bottom: 30, left: 10 }}>
          <XAxis
            dataKey="name"
            stroke="#64748b"
            fontSize={10}
            tickLine={false}
            interval={0}
            angle={-15}
            textAnchor="end"
          />
          <YAxis stroke="#64748b" fontSize={10} tickLine={false} unit="%" />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg text-xs font-mono shadow-xl">
                    <p className="text-white font-bold mb-1">{data.name}</p>
                    <p className="text-rose-400">Shift: {data.changePct.toFixed(1)}%</p>
                    <p className="text-indigo-400">Share of Drop: {data.contributionPct.toFixed(1)}%</p>
                    <p className="text-slate-400">Evidence Score: {data.score}/100</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="contributionPct" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.changePct < 0 ? '#f43f5e' : '#10b981'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
