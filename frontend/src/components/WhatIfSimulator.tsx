import React, { useState } from 'react';
import { Sliders, TrendingUp, Sparkles, RefreshCw } from 'lucide-react';
import { simulateScenario } from '../services/api';

interface WhatIfSimulatorProps {
  datasetId: string;
  targetMetric: string;
  driverVariables: string[];
}

export const WhatIfSimulator: React.FC<WhatIfSimulatorProps> = ({ datasetId, targetMetric, driverVariables }) => {
  const [adjustments, setAdjustments] = useState<Record<string, number>>({});
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const handleSliderChange = (driver: string, value: number) => {
    const updated = { ...adjustments, [driver]: value };
    setAdjustments(updated);
  };

  const runSimulation = async () => {
    if (!datasetId) return;
    setIsSimulating(true);
    try {
      const activeAdjustments: Record<string, number> = {};
      Object.keys(adjustments).forEach((key) => {
        if (adjustments[key] !== 0) {
          activeAdjustments[key] = adjustments[key];
        }
      });
      const result = await simulateScenario(datasetId, targetMetric, activeAdjustments);
      setSimulationResult(result);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setAdjustments({});
    setSimulationResult(null);
  };

  const activeDrivers = driverVariables.filter((d) => d !== targetMetric).slice(0, 4);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-md space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-indigo-400" />
            Interactive "What-If" Scenario Simulator
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Adjust operational driver variables to simulate counterfactual recovery on{' '}
            <strong className="text-indigo-300 uppercase">{targetMetric}</strong>.
          </p>
        </div>
        <button
          onClick={handleReset}
          className="text-xs font-mono text-slate-400 hover:text-white flex items-center gap-1 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 transition-all"
        >
          <RefreshCw className="w-3 h-3" /> Reset
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sliders Area */}
        <div className="space-y-4 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <span className="text-[10px] font-mono uppercase tracking-wider text-indigo-400 block mb-2">
            Operational Driver Adjustments
          </span>

          {activeDrivers.length === 0 && (
            <p className="text-xs text-slate-500 italic">No additional numeric driver variables detected.</p>
          )}

          {activeDrivers.map((driver) => {
            const val = adjustments[driver] || 0;
            return (
              <div key={driver} className="space-y-1.5">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-slate-300 capitalize">{driver.replace(/_/g, ' ')}</span>
                  <span className={`font-bold ${val > 0 ? 'text-emerald-400' : val < 0 ? 'text-rose-400' : 'text-slate-400'}`}>
                    {val > 0 ? `+${val}` : val}
                  </span>
                </div>
                <input
                  type="range"
                  min="-10"
                  max="10"
                  step="0.5"
                  value={val}
                  onChange={(e) => handleSliderChange(driver, parseFloat(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                />
              </div>
            );
          })}

          <button
            onClick={runSimulation}
            disabled={isSimulating || activeDrivers.length === 0}
            className="w-full py-2.5 mt-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4" /> {isSimulating ? 'Simulating Counterfactual...' : 'Run Simulation'}
          </button>
        </div>

        {/* Results Area */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 block mb-2">
              Predicted Counterfactual Outcome
            </span>

            {simulationResult ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 block">BASELINE MEAN</span>
                    <span className="text-lg font-bold font-mono text-slate-300">
                      {simulationResult.baseline_mean}
                    </span>
                  </div>
                  <TrendingUp className="w-5 h-5 text-slate-600" />
                  <div className="text-right">
                    <span className="text-[10px] font-mono text-slate-500 block">SIMULATED MEAN</span>
                    <span className="text-xl font-extrabold font-mono text-emerald-400">
                      {simulationResult.simulated_mean}
                    </span>
                  </div>
                </div>

                <div className="p-3 bg-indigo-950/30 border border-indigo-500/30 rounded-lg text-xs text-indigo-300 font-mono">
                  {simulationResult.scenario_summary}
                </div>

                <div className="space-y-2">
                  <span className="text-[10px] font-mono text-slate-400 uppercase">Impact Breakdown:</span>
                  {simulationResult.variable_impacts?.map((imp: any, idx: number) => (
                    <div key={idx} className="flex justify-between items-center text-xs font-mono bg-slate-900 p-2 rounded border border-slate-800">
                      <span className="text-slate-300 capitalize">{imp.driver_variable.replace(/_/g, ' ')}</span>
                      <span className={imp.percentage_impact >= 0 ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}>
                        {imp.percentage_impact >= 0 ? `+${imp.percentage_impact}%` : `${imp.percentage_impact}%`}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="h-40 flex flex-col items-center justify-center text-center text-slate-500 space-y-2">
                <Sliders className="w-8 h-8 opacity-30 text-indigo-400" />
                <p className="text-xs">Adjust sliders and click "Run Simulation" to model recovery impact.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
