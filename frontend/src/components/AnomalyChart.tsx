import React from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
  Cell
} from 'recharts';

interface AnomalyChartProps {
  anomalies: any[];
}

export const AnomalyChart: React.FC<AnomalyChartProps> = ({ anomalies }) => {
  if (!anomalies || anomalies.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-xs text-slate-500 font-mono">
        No anomalous data points detected.
      </div>
    );
  }

  const chartData = anomalies.map((item, idx) => ({
    x: idx + 1,
    y: item.value,
    score: item.score,
    severity: item.severity,
    row: item.row_identifier || item.row_index,
    column: item.column
  }));

  const getSeverityColor = (severity: string) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL': return '#f43f5e';
      case 'HIGH': return '#f97316';
      case 'MEDIUM': return '#eab308';
      default: return '#3b82f6';
    }
  };

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
          <XAxis dataKey="x" name="Record" stroke="#64748b" fontSize={10} tickLine={false} />
          <YAxis dataKey="y" name="Value" stroke="#64748b" fontSize={10} tickLine={false} />
          <ZAxis dataKey="score" range={[60, 300]} name="Anomaly Score" />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg text-xs font-mono shadow-xl">
                    <p className="text-white font-bold mb-1">Record: {data.row}</p>
                    <p className="text-slate-400">Column: {data.column}</p>
                    <p className="text-slate-400">Value: {data.y.toLocaleString()}</p>
                    <p className="text-slate-400">Score: {data.score.toFixed(1)}/100</p>
                    <p className="mt-1 font-bold uppercase" style={{ color: getSeverityColor(data.severity) }}>
                      Severity: {data.severity}
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Scatter name="Anomalies" data={chartData}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getSeverityColor(entry.severity)} />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};
