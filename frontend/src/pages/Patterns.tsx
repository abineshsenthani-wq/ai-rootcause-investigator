import React, { useState, useEffect } from 'react';
import { GitCommit, TrendingDown, BarChart2, Zap, ArrowRight, ShieldCheck, Activity } from 'lucide-react';
import { DatasetMeta } from '../types';
import { runInvestigation } from '../services/api';

export const PatternsPage: React.FC<{ currentDataset: DatasetMeta | null }> = ({ currentDataset }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [correlations, setCorrelations] = useState<any[]>([]);
  const [causalDrivers, setCausalDrivers] = useState<any[]>([]);
  const [targetMetric, setTargetMetric] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (currentDataset?.id) {
      setLoading(true);
      setError(null);
      runInvestigation(currentDataset.id)
        .then((res) => {
          setCorrelations(res.evidence || []);
          setCausalDrivers(res.causal_inference || []);
          setTargetMetric(res.event?.metric || currentDataset.primary_metric || 'metric');
        })
        .catch((err) => {
          setError(err.message || 'Could not load correlation patterns.');
        })
        .finally(() => setLoading(false));
    }
  }, [currentDataset?.id]);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-md">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <GitCommit className="w-5 h-5 text-indigo-400" />
          Pattern, Correlation & Causal Inference Engine
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Dynamically computes Pearson linear association, Spearman rank co-variance (with Student's t p-values &amp; 95% Fisher Confidence Intervals), and Granger Causality temporal lead-lag tests across active dataset columns.
        </p>
      </div>

      {error && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400 text-xs font-mono">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center p-12 bg-slate-900 rounded-xl border border-slate-800 text-slate-400 text-xs gap-3">
          <Activity className="w-4 h-4 animate-spin text-indigo-400" />
          Calculating live Pearson correlations and Granger causality tests...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pearson / Spearman Matrix Card */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4 shadow-md">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-indigo-400" />
                Empirical Co-variance Matrix ({targetMetric.toUpperCase()})
              </h3>
              <span className="text-[11px] text-slate-500 font-mono">
                {correlations.length} Metric Pair(s)
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Measures linear and monotonic co-movement against primary target metric <span className="font-semibold text-slate-300 font-mono">{targetMetric}</span>.
            </p>

            {correlations.length === 0 ? (
              <div className="p-6 bg-slate-950/60 rounded-lg border border-slate-850 text-center text-xs text-slate-500">
                No secondary continuous numerical metrics available for correlation analysis in this dataset.
              </div>
            ) : (
              <div className="space-y-2.5 text-xs font-mono">
                {correlations.map((c: any, idx: number) => {
                  const r = c.pearson_correlation ?? 0;
                  const isPositive = r >= 0;
                  const colorClass =
                    Math.abs(r) >= 0.5
                      ? isPositive
                        ? 'text-emerald-400'
                        : 'text-rose-400'
                      : 'text-amber-400';

                  return (
                    <div
                      key={idx}
                      className="p-3.5 bg-slate-950/80 rounded-lg border border-slate-800 flex flex-col sm:flex-row justify-between sm:items-center gap-2"
                    >
                      <div>
                        <div className="text-slate-200 font-semibold flex items-center gap-1.5 capitalize">
                          <span>{targetMetric.replace('_', ' ')}</span>
                          <ArrowRight className="w-3 h-3 text-slate-600" />
                          <span className="text-indigo-300">{c.correlated_variable.replace('_', ' ')}</span>
                        </div>
                        <div className="text-[10px] text-slate-500 mt-1">
                          p-value: {c.p_value != null ? Number(c.p_value).toFixed(4) : 'N/A'} • 95% CI [{c.confidence_interval_95?.[0]?.toFixed(2) ?? '0.00'}, {c.confidence_interval_95?.[1]?.toFixed(2) ?? '0.00'}]
                        </div>
                      </div>

                      <div className="text-right">
                        <span className={`text-sm font-bold ${colorClass}`}>
                          {isPositive ? `+${Number(r).toFixed(2)}` : Number(r).toFixed(2)}
                        </span>
                        <span className="text-[10px] text-slate-500 block uppercase font-sans">
                          {c.relationship_strength || 'Correlation'}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Granger Causality Card */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4 shadow-md flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                  <Zap className="w-4 h-4 text-amber-400" />
                  Granger Causality Temporal Leads
                </h3>
                <span className="text-[11px] text-slate-500 font-mono">VAR F-Test</span>
              </div>
              <p className="text-xs text-slate-400">
                Tests if prior shifts in operational indicators statistically forecast future changes in <span className="font-semibold text-slate-300 font-mono">{targetMetric}</span> (Temporal Precedence).
              </p>

              {causalDrivers.length === 0 ? (
                <div className="p-6 bg-slate-950/60 rounded-lg border border-slate-850 text-center text-xs text-slate-500">
                  No lagged temporal causal drivers isolated for this dataset time-series.
                </div>
              ) : (
                <div className="space-y-2.5 text-xs font-mono">
                  {causalDrivers.map((cd: any, idx: number) => (
                    <div
                      key={idx}
                      className={`p-3.5 rounded-lg border flex justify-between items-center ${
                        cd.is_causal
                          ? 'bg-amber-950/20 border-amber-500/30'
                          : 'bg-slate-950/60 border-slate-850'
                      }`}
                    >
                      <div>
                        <div className="font-semibold text-slate-200 flex items-center gap-2">
                          <span className="capitalize">{cd.driver_variable.replace('_', ' ')}</span>
                          {cd.is_causal && (
                            <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-300 font-sans">
                              Significant Lead
                            </span>
                          )}
                        </div>
                        <div className="text-[10px] text-slate-500 mt-1">
                          Lag: {cd.best_lag_periods} Period(s) • F-Stat: {cd.f_statistic} • p: {Number(cd.p_value).toFixed(4)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Methodological Context Note */}
            <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800 text-xs space-y-1 mt-4">
              <div className="text-slate-300 font-semibold flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                Grounded Statistical Boundaries
              </div>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Correlation identifies contemporaneous co-variance; Granger testing establishes temporal lead-lag association. The system strictly separates verified facts from observational hypotheses.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
