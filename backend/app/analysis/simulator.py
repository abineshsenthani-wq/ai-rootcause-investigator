import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List

class WhatIfSimulator:
    """
    Simulates counterfactual scenarios ('What-If' analysis) by modeling sensitivity
    coefficients between driver variables and target metrics.
    """

    @classmethod
    def simulate_counterfactual(
        cls,
        df: pd.DataFrame,
        target_metric: str,
        driver_adjustments: Dict[str, float]
    ) -> Dict[str, Any]:
        if target_metric not in df.columns or df.empty:
            return {"status": "error", "message": "Target metric not found in dataset."}

        num_df = df.select_dtypes(include=[np.number]).dropna()
        if target_metric not in num_df.columns:
            return {"status": "error", "message": "Target metric must be numeric."}

        baseline_mean = float(num_df[target_metric].mean())
        baseline_std = float(num_df[target_metric].std())
        simulated_mean = baseline_mean

        variable_impacts = []

        for driver, delta in driver_adjustments.items():
            if driver not in num_df.columns or driver == target_metric:
                continue

            driver_mean = float(num_df[driver].mean())
            driver_std = float(num_df[driver].std())

            if driver_std == 0:
                continue

            # Linear regression sensitivity coefficient (slope)
            slope, intercept, r_val, p_val, std_err = stats.linregress(num_df[driver], num_df[target_metric])

            marginal_impact = slope * delta
            pct_impact = (marginal_impact / baseline_mean * 100) if baseline_mean != 0 else 0.0
            simulated_mean += marginal_impact

            variable_impacts.append({
                "driver_variable": driver,
                "user_adjustment_delta": delta,
                "marginal_metric_change": round(float(marginal_impact), 2),
                "percentage_impact": round(float(pct_impact), 2),
                "regression_slope": round(float(slope), 4),
                "p_value": round(float(p_val), 5),
                "statistically_significant": p_val < 0.05
            })

        total_delta = simulated_mean - baseline_mean
        total_pct_change = (total_delta / baseline_mean * 100) if baseline_mean != 0 else 0.0

        return {
            "target_metric": target_metric,
            "baseline_mean": round(baseline_mean, 2),
            "simulated_mean": round(simulated_mean, 2),
            "total_predicted_change": round(total_delta, 2),
            "total_percentage_impact": round(total_pct_change, 2),
            "variable_impacts": variable_impacts,
            "scenario_summary": (
                f"Adjusting variables ({', '.join(driver_adjustments.keys())}) is predicted to shift "
                f"'{target_metric}' from {baseline_mean:.2f} to {simulated_mean:.2f} ({total_pct_change:+.2f}%)."
            )
        }
