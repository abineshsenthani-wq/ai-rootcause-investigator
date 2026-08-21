import React from 'react';
import { CheckCircle2, HelpCircle, Lightbulb } from 'lucide-react';

interface FindingCardProps {
  type: 'FACT' | 'HYPOTHESIS' | 'RECOMMENDATION';
  title?: string;
  statement: string;
  evidenceScore?: number;
}

export const FindingCard: React.FC<FindingCardProps> = ({
  type,
  title,
  statement,
  evidenceScore
}) => {
  const configs = {
    FACT: {
      badge: 'FACT',
      badgeBg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
      icon: CheckCircle2,
      border: 'border-slate-800 hover:border-emerald-500/40'
    },
    HYPOTHESIS: {
      badge: 'HYPOTHESIS',
      badgeBg: 'bg-indigo-500/10 border-indigo-500/30 text-indigo-400',
      icon: HelpCircle,
      border: 'border-slate-800 hover:border-indigo-500/40'
    },
    RECOMMENDATION: {
      badge: 'RECOMMENDATION',
      badgeBg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      icon: Lightbulb,
      border: 'border-slate-800 hover:border-amber-500/40'
    }
  };

  const config = configs[type] || configs.FACT;
  const Icon = config.icon;

  return (
    <div className={`bg-slate-900 border ${config.border} rounded-xl p-4 transition-colors shadow-sm`}>
      <div className="flex items-center justify-between mb-2">
        <span className={`text-[10px] font-mono font-bold uppercase px-2 py-0.5 border rounded ${config.badgeBg}`}>
          {config.badge}
        </span>
        {evidenceScore !== undefined && (
          <span className="text-[10px] font-mono text-slate-400 bg-slate-950 px-2 py-0.5 border border-slate-850 rounded">
            Score: {evidenceScore}/100
          </span>
        )}
      </div>

      <div className="flex items-start gap-3 mt-2">
        <Icon className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
        <div>
          {title && <h4 className="text-xs font-semibold text-white mb-1">{title}</h4>}
          <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{statement}</p>
        </div>
      </div>
    </div>
  );
};
