import React from 'react';
import { ArrowDown, Layers } from 'lucide-react';

interface FactorNode {
  factor_name: string;
  dimension: string;
  segment: string;
  metric_change_pct: number;
  contribution_pct: number;
  evidence_score: number;
  evidence_label: string;
}

interface EvidenceGraphProps {
  metricName?: string;
  percentageChange?: number;
  factors?: FactorNode[];
  investigation?: any;
}

export const EvidenceGraph: React.FC<EvidenceGraphProps> = ({ metricName, percentageChange, factors, investigation }) => {
  const actualMetricName = metricName || investigation?.event?.metric || 'revenue';
  const actualPercentageChange = percentageChange ?? investigation?.event?.percentage_change ?? -24.1;
  const actualFactors = factors || investigation?.ranked_factors || investigation?.factors || [];

  const topFactor = actualFactors[0] || {
    factor_name: 'West Region Breakdown',
    dimension: 'region',
    segment: 'West',
    metric_change_pct: -41.8,
    contribution_pct: 42.0,
    evidence_score: 88.0,
    evidence_label: 'HIGH EVIDENCE'
  };

  const secondFactor = actualFactors[1] || {
    factor_name: 'Product C Drop',
    dimension: 'product_id',
    segment: 'Prod_C',
    metric_change_pct: -36.2,
    contribution_pct: 31.0,
    evidence_score: 82.0,
    evidence_label: 'HIGH EVIDENCE'
  };

  const thirdFactor = actualFactors[2] || {
    factor_name: 'Delivery Days Co-Variance',
    dimension: 'numerical_correlation',
    segment: 'delivery_days',
    metric_change_pct: 31.0,
    contribution_pct: 0.0,
    evidence_score: 74.0,
    evidence_label: 'HIGH EVIDENCE'
  };

  return (
    <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-indigo-400" />
          Interactive Root-Cause Evidence Graph
        </h3>
        <span className="text-[10px] bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 px-2.5 py-1 rounded-full font-mono">
          Decomposition Flow
        </span>
      </div>

      <div className="flex flex-col md:flex-row items-center justify-between gap-4 py-4 px-2">
        {/* Node 1: Root Metric Event */}
        <div className="w-full md:w-56 bg-slate-950 p-4 rounded-xl border border-rose-500/40 shadow-lg text-center relative group hover:border-rose-400 transition-all">
          <span className="text-[10px] uppercase font-mono text-rose-400 tracking-wider block">Target Metric Event</span>
          <h4 className="text-base font-bold text-white mt-1 capitalize">{actualMetricName} Decline</h4>
          <div className="mt-2 text-xl font-extrabold text-rose-400 font-mono">
            {actualPercentageChange > 0 ? `+${actualPercentageChange.toFixed(1)}%` : `${actualPercentageChange.toFixed(1)}%`}
          </div>
          <div className="mt-1 text-[10px] text-slate-500 font-mono">Overall Metric Shift</div>
        </div>

        {/* Edge Connector 1 */}
        <div className="flex md:flex-col items-center text-slate-600">
          <ArrowDown className="w-6 h-6 rotate-[-90deg] md:rotate-0 text-indigo-500 animate-pulse" />
        </div>

        {/* Node 2: Primary Segment Contribution */}
        <div className="w-full md:w-56 bg-slate-950 p-4 rounded-xl border border-indigo-500/40 shadow-lg text-center relative group hover:border-indigo-400 transition-all">
          <span className="text-[10px] uppercase font-mono text-indigo-400 tracking-wider block">Primary Segment Loss</span>
          <h4 className="text-sm font-bold text-white mt-1 truncate">{topFactor.segment || 'West Region'}</h4>
          <div className="mt-2 text-sm font-bold text-indigo-400 font-mono">
            {topFactor.contribution_pct}% Share of Loss
          </div>
          <div className="mt-1 text-[10px] text-slate-400">Score: {topFactor.evidence_score}/100</div>
        </div>

        {/* Edge Connector 2 */}
        <div className="flex md:flex-col items-center text-slate-600">
          <ArrowDown className="w-6 h-6 rotate-[-90deg] md:rotate-0 text-indigo-500 animate-pulse" />
        </div>

        {/* Node 3: Secondary Product Category */}
        <div className="w-full md:w-56 bg-slate-950 p-4 rounded-xl border border-amber-500/40 shadow-lg text-center relative group hover:border-amber-400 transition-all">
          <span className="text-[10px] uppercase font-mono text-amber-400 tracking-wider block">Affected Sub-Category</span>
          <h4 className="text-sm font-bold text-white mt-1 truncate">{secondFactor.segment || 'Product C'}</h4>
          <div className="mt-2 text-sm font-bold text-amber-400 font-mono">
            {secondFactor.metric_change_pct}% Metric Drop
          </div>
          <div className="mt-1 text-[10px] text-slate-400">Score: {secondFactor.evidence_score}/100</div>
        </div>

        {/* Edge Connector 3 */}
        <div className="flex md:flex-col items-center text-slate-600">
          <ArrowDown className="w-6 h-6 rotate-[-90deg] md:rotate-0 text-indigo-500 animate-pulse" />
        </div>

        {/* Node 4: Co-varying Operational Variable */}
        <div className="w-full md:w-56 bg-slate-950 p-4 rounded-xl border border-emerald-500/40 shadow-lg text-center relative group hover:border-emerald-400 transition-all">
          <span className="text-[10px] uppercase font-mono text-emerald-400 tracking-wider block">Associated Driver</span>
          <h4 className="text-sm font-bold text-white mt-1 truncate">{thirdFactor.segment || 'Delivery Days'}</h4>
          <div className="mt-2 text-sm font-bold text-emerald-400 font-mono">
            Co-variance Spike
          </div>
          <div className="mt-1 text-[10px] text-slate-400">Score: {thirdFactor.evidence_score}/100</div>
        </div>
      </div>
    </div>
  );
};
