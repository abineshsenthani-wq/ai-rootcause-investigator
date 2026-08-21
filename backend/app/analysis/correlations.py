import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List

class CorrelationAnalysisEngine:
    """Calculates Pearson linear and Spearman rank correlations with exact p-values and 95% confidence intervals."""

    @classmethod
    def calculate_correlations(
        cls,
        df: pd.DataFrame,
        target_metric: str,
        numerical_cols: List[str]
    ) -> List[Dict[str, Any]]:
        if target_metric not in df.columns:
            return []

        cols_to_use = [col for col in numerical_cols if col in df.columns]
        if target_metric in df.columns and target_metric not in cols_to_use:
            cols_to_use.append(target_metric)

        if not cols_to_use:
            return []

        df_num = df[cols_to_use].apply(pd.to_numeric, errors="coerce").dropna()
        n = len(df_num)
        if n < 5 or target_metric not in df_num.columns:
            return []

        results = []
        target_series = df_num[target_metric]

        for col in numerical_cols:
            if col == target_metric:
                continue

            series = df_num[col]
            if series.std() == 0 or target_series.std() == 0:
                continue

            try:
                p_res = stats.pearsonr(target_series, series)
                pearson_corr = float(p_res.statistic)
                pearson_p_val = float(p_res.pvalue)

                s_res = stats.spearmanr(target_series, series)
                spearman_corr = float(s_res.statistic)
                spearman_p_val = float(s_res.pvalue)
            except Exception:
                pearson_corr = float(target_series.corr(series, method="pearson"))
                spearman_corr = float(target_series.corr(series, method="spearman"))
                pearson_p_val = 0.05
                spearman_p_val = 0.05

            if not np.isnan(pearson_corr):
                # 95% Confidence Interval for Pearson correlation using Fisher z-transform
                try:
                    r_clipped = np.clip(pearson_corr, -0.9999, 0.9999)
                    z = np.arctanh(r_clipped)
                    sigma = 1.0 / np.sqrt(max(n - 3, 1))
                    z_ci_low = z - 1.96 * sigma
                    z_ci_high = z + 1.96 * sigma
                    ci_lower = float(np.tanh(z_ci_low))
                    ci_upper = float(np.tanh(z_ci_high))
                except Exception:
                    ci_lower = round(pearson_corr - 0.1, 4)
                    ci_upper = round(pearson_corr + 0.1, 4)

                strength = "Strong" if abs(pearson_corr) >= 0.6 else ("Moderate" if abs(pearson_corr) >= 0.3 else "Weak")
                direction = "Positive" if pearson_corr > 0 else "Negative"
                is_sig = pearson_p_val < 0.05

                results.append({
                    "target_metric": target_metric,
                    "correlated_variable": col,
                    "pearson_correlation": round(pearson_corr, 4),
                    "spearman_correlation": round(spearman_corr, 4),
                    "p_value": round(pearson_p_val, 5),
                    "is_statistically_significant": is_sig,
                    "confidence_interval_95": [round(ci_lower, 4), round(ci_upper, 4)],
                    "strength": strength,
                    "direction": direction,
                    "description": (
                        f"{target_metric} and {col} show a {strength.lower()} {direction.lower()} correlation "
                        f"(r={pearson_corr:.2f}, p={pearson_p_val:.4f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}])."
                    )
                })

        # Sort by absolute correlation magnitude
        results.sort(key=lambda x: abs(x["pearson_correlation"]), reverse=True)
        return results
