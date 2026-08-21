import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badge?: {
    text: string;
    type?: 'positive' | 'negative' | 'neutral' | 'warning';
  };
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge
}) => {
  const badgeStyles = {
    positive: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
    negative: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
    warning: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
    neutral: 'bg-slate-800 border-slate-700 text-slate-300'
  };

  const badgeClass = badge ? badgeStyles[badge.type || 'neutral'] : '';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider font-mono">
          {title}
        </span>
        <div className="p-2 bg-slate-950 rounded-lg border border-slate-850 text-indigo-400">
          <Icon className="w-4 h-4" />
        </div>
      </div>

      <div className="flex items-baseline justify-between">
        <h3 className="text-2xl font-bold text-white tracking-tight">{value}</h3>
        {badge && (
          <span className={`text-xs px-2 py-0.5 border rounded-md font-mono font-semibold ${badgeClass}`}>
            {badge.text}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-2 text-xs text-slate-500 font-mono">{subtitle}</p>
      )}
    </div>
  );
};
