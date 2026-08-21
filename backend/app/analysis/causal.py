import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional

class GrangerCausalityEngine:
    """
    Evaluates temporal lead-lag relationships and Granger Causality (F-test p-values)
    to distinguish genuine causal drivers from simple contemporaneous co-variance.
    """

    @classmethod
    def test_causality(
        cls,
        df: pd.DataFrame,
        date_col: Optional[str],
        target_metric: str,
        numerical_cols: List[str],
        max_lag: int = 3
    ) -> List[Dict[str, Any]]:
        if target_metric not in df.columns or len(df) < 10:
            return []

        # Sort by date if available
        df_clean = df.copy()
        if date_col and date_col in df_clean.columns:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")
            df_clean = df_clean.dropna(subset=[date_col]).sort_values(by=date_col)

        causal_results = []
        target_series = df_clean[target_metric].astype(float)

        for col in numerical_cols:
            if col == target_metric:
                continue

            driver_series = df_clean[col].astype(float)

            # Drop missing values
            valid_mask = ~(target_series.isna() | driver_series.isna())
            y = target_series[valid_mask].values
            x = driver_series[valid_mask].values

            if len(y) < 10 or np.std(x) == 0 or np.std(y) == 0:
                continue

            best_lag = 0
            best_p_val = 1.0
            best_f_stat = 0.0

            # Test Granger Causality for lags 1 to max_lag
            for lag in range(1, min(max_lag + 1, len(y) // 3)):
                try:
                    n = len(y) - lag
                    Y_target = y[lag:]
                    Y_lags = np.column_stack([y[lag - i : n + lag - i] for i in range(1, lag + 1)])
                    X_lags = np.column_stack([x[lag - i : n + lag - i] for i in range(1, lag + 1)])

                    # Restricted model: Y_target ~ Y_lags
                    X_restr = np.column_stack([np.ones(n), Y_lags])
                    beta_restr, _, _, _ = np.linalg.lstsq(X_restr, Y_target, rcond=None)
                    res_restr = Y_target - X_restr @ beta_restr
                    rss1 = np.sum(res_restr ** 2)

                    # Unrestricted model: Y_target ~ Y_lags + X_lags
                    X_unrestr = np.column_stack([np.ones(n), Y_lags, X_lags])
                    beta_unrestr, _, _, _ = np.linalg.lstsq(X_unrestr, Y_target, rcond=None)
                    res_unrestr = Y_target - X_unrestr @ beta_unrestr
                    rss2 = np.sum(res_unrestr ** 2)

                    df1 = lag
                    df2 = n - (2 * lag + 1)
                    if df2 > 0 and rss2 > 0:
                        f_stat = ((rss1 - rss2) / df1) / (rss2 / df2)
                        p_val = stats.f.sf(f_stat, df1, df2)

                        if p_val < best_p_val:
                            best_p_val = float(p_val)
                            best_f_stat = float(f_stat)
                            best_lag = lag
                except Exception:
                    continue

            is_causal = best_p_val < 0.05
            classification = (
                "Verified Granger Causal Lead" if is_causal
                else ("Likely Causal Lead" if best_p_val < 0.10 else "Contemporaneous Co-variance Only")
            )

            causal_results.append({
                "driver_variable": col,
                "target_metric": target_metric,
                "best_lag_periods": best_lag,
                "f_statistic": round(best_f_stat, 4),
                "p_value": round(best_p_val, 5),
                "is_causal": is_causal,
                "statistically_significant": best_p_val < 0.05,
                "causal_classification": classification,
                "explanation": (
                    f"Past shifts in '{col}' at a lag of {best_lag} period(s) significantly predict "
                    f"future shifts in '{target_metric}' (p={best_p_val:.4f})."
                    if is_causal else
                    f"No statistically significant Granger causality lead detected for '{col}' (p={best_p_val:.4f})."
                )
            })

        causal_results.sort(key=lambda item: item["p_value"])
        return causal_results
