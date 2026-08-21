import React from 'react';
import { Sparkles, Shield, ArrowDownRight, ArrowUpRight, Cpu, History, Zap } from 'lucide-react';
import { FindingCard } from './FindingCard';
import { EvidenceGraph } from './Investigation/EvidenceGraph';
import { WhatIfSimulator } from './WhatIfSimulator';
import { ForecastChart } from './ForecastChart';

interface InvestigationPanelProps {
  investigation: any;
  datasetId?: string;
}

export const InvestigationPanel: React.FC<InvestigationPanelProps> = ({ investigation, datasetId }) => {
  if (!investigation) return null;

  const event = investigation.event || {};
  const isDrop = (event.percentage_change || 0) < 0;
  const targetMetric = event.metric || 'revenue';
  const causalLeads = investigation.causal_inference || [];
  const similarIncidents = investigation.similar_incidents || [];
  const driverVars = investigation.evidence?.map((e: any) => e.correlated_variable) || [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] font-mono uppercase tracking-wider px-2.5 py-0.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full flex items-center gap-1">
                <Cpu className="w-3 h-3 text-indigo-400" /> Multi-Agent Causal Findings
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Metric: <strong className="text-white uppercase font-sans">{targetMetric}</strong>
              </span>
            </div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              {isDrop ? (
                <ArrowDownRight className="w-6 h-6 text-rose-500" />
              ) : (
                <ArrowUpRight className="w-6 h-6 text-emerald-500" />
              )}
              {event.event_type || 'METRIC_SHIFT'}: {event.percentage_change?.toFixed(1)}% shift
            </h2>
            <p className="text-xs text-slate-400 font-mono mt-1">
              Window: {event.start_period} → {event.end_period}
            </p>
          </div>

          <div className="flex items-center gap-4 bg-slate-950/70 border border-slate-800 p-4 rounded-xl">
            <div className="text-right">
              <span className="text-[10px] text-slate-500 font-mono block">EVIDENCE CONFIDENCE</span>
              <span className="text-xl font-bold font-mono text-indigo-400">
                {investigation.confidence}%
              </span>
            </div>
            <Shield className="w-8 h-8 text-indigo-400" />
          </div>
        </div>
      </div>

      {/* Visual Evidence Flow Graph */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-indigo-400" /> Grounded Evidence Flow Graph
        </h3>
        <EvidenceGraph investigation={investigation} />
      </div>

      {/* Granger Causality & Statistical Rigor Section */}
      {causalLeads.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" /> Granger Causality Lead-Lag Tests ($X \to Y$)
            </h3>
            <span className="text-[10px] font-mono text-slate-400 bg-slate-950 px-2.5 py-1 rounded-full border border-slate-800">
              Temporal F-Test Evaluation
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {causalLeads.map((c: any, idx: number) => (
              <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                <div className="flex justify-between items-start">
                  <span className="text-xs font-bold text-white capitalize">{c.driver_variable?.replace(/_/g, ' ')}</span>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${c.is_causal ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'}`}>
                    {c.causal_classification}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed font-mono">{c.explanation}</p>
                <div className="flex items-center gap-4 text-[10px] font-mono text-slate-500 pt-1 border-t border-slate-900">
                  <span>F-Stat: <strong className="text-slate-300">{c.f_statistic}</strong></span>
                  <span>p-Value: <strong className={c.statistically_significant ? 'text-emerald-400 font-bold' : 'text-slate-400'}>{c.p_value}</strong></span>
                  <span>Lag: <strong className="text-slate-300">{c.best_lag_periods} period(s)</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Time-Series Forecast Chart */}
      {datasetId && <ForecastChart datasetId={datasetId} targetMetric={targetMetric} />}

      {/* Interactive What-If Scenario Simulator */}
      {datasetId && (
        <WhatIfSimulator datasetId={datasetId} targetMetric={targetMetric} driverVariables={driverVars} />
      )}

      {/* RAG Historical Vector Memory Precedents */}
      {similarIncidents.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <History className="w-4 h-4 text-sky-400" /> RAG Historical Incident Precedents (Vector Memory)
            </h3>
            <span className="text-[10px] font-mono text-sky-400 bg-sky-500/10 px-2.5 py-1 rounded-full border border-sky-500/30">
              Cosine Similarity Search
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {similarIncidents.map((inc: any, idx: number) => (
              <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-sky-300">{inc.dataset_name}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 bg-sky-500/20 text-sky-300 rounded-full">
                    Match: {(inc.similarity_score * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-xs text-slate-300 font-mono">{inc.summary}</p>
                <div className="text-[10px] font-mono text-slate-500">
                  Historical Driver: <strong className="text-slate-400">{inc.primary_driver}</strong>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Executive Synthesis */}
      {investigation.ai_explanation && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" /> AI Executive Synthesis (Multi-Agent Grounded)
          </h3>
          <div className="text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap bg-slate-950 p-4 rounded-xl border border-slate-850">
            {investigation.ai_explanation}
          </div>
        </div>
      )}

      {/* Facts vs Hypotheses vs Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Facts */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-emerald-400 font-mono uppercase tracking-wider">
            Verified Facts ({investigation.facts?.length || 0})
          </h4>
          {investigation.facts?.map((fact: string, idx: number) => (
            <FindingCard key={idx} type="FACT" statement={fact} />
          ))}
        </div>

        {/* Hypotheses */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-indigo-400 font-mono uppercase tracking-wider">
            Supported Hypotheses ({investigation.hypotheses?.length || 0})
          </h4>
          {investigation.hypotheses?.map((h: any, idx: number) => (
            <FindingCard
              key={idx}
              type="HYPOTHESIS"
              statement={h.statement || h}
              evidenceScore={h.evidence_score}
            />
          ))}
        </div>

        {/* Recommendations */}
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-amber-400 font-mono uppercase tracking-wider">
            Actionable Next Steps ({investigation.recommendations?.length || 0})
          </h4>
          {investigation.recommendations?.map((rec: string, idx: number) => (
            <FindingCard key={idx} type="RECOMMENDATION" statement={rec} />
          ))}
        </div>
      </div>
    </div>
  );
};
