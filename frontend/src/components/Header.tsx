import React from 'react';
import { Database, Sparkles, Activity, ShieldCheck } from 'lucide-react';
import { DatasetMeta } from '../types';

interface HeaderProps {
  currentDataset: DatasetMeta | null;
}

export const Header: React.FC<HeaderProps> = ({ currentDataset }) => {
  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300">
          <Database className="w-3.5 h-3.5 text-indigo-400" />
          <span>Active Dataset:</span>
          <strong className="text-white font-semibold">
            {currentDataset ? currentDataset.filename : 'None Loaded'}
          </strong>
        </div>

        {currentDataset && (
          <span className="text-[11px] text-slate-400 font-mono hidden md:inline">
            ({currentDataset.row_count.toLocaleString()} rows • {currentDataset.column_count} cols)
          </span>
        )}
      </div>

      <div className="flex items-center gap-3">
        <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full text-xs font-mono flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5" /> Engine Operational
        </span>
        <span className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 rounded-full text-xs font-mono flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5" /> Deterministic ML Active
        </span>
      </div>
    </header>
  );
};
