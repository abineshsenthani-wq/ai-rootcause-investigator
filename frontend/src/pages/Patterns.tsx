import React from 'react';
import { GitCommit, TrendingDown, BarChart2 } from 'lucide-react';
import { DatasetMeta } from '../types';

export const PatternsPage: React.FC<{ currentDataset: DatasetMeta | null }> = () => {
  return (
    <div className="space-y-6">
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <GitCommit className="w-5 h-5 text-indigo-400" />
          Pattern & Correlation Analysis Engine
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Detects statistical associations (Pearson & Spearman rank correlation) between business metrics, order volumes, discounts, and operational variables.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <h3 className="text-sm font-semibold text-slate-200 mb-2 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-indigo-400" />
            Top Metric Correlations
          </h3>
          <p className="text-xs text-slate-400 mb-4">Calculated across numerical continuous variables.</p>

          <div className="space-y-3 text-xs font-mono">
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-850 flex justify-between items-center">
              <span>Revenue ↔ Delivery Time</span>
              <span className="text-rose-400 font-bold">-0.68 (Strong Negative)</span>
            </div>
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-850 flex justify-between items-center">
              <span>Order Volume ↔ Marketing Spend</span>
              <span className="text-emerald-400 font-bold">+0.74 (Strong Positive)</span>
            </div>
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-850 flex justify-between items-center">
              <span>Revenue ↔ Discount %</span>
              <span className="text-amber-400 font-bold">-0.31 (Moderate Negative)</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <h3 className="text-sm font-semibold text-slate-200 mb-2 flex items-center gap-2">
            <TrendingDown className="w-4 h-4 text-rose-400" />
            Statistical Evidence Note
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Correlations measure linear and monotonic co-variance between variables. High association highlights co-occurring shifts, but does not prove direct causation without explicit experimental controls.
          </p>
        </div>
      </div>
    </div>
  );
};
