import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional

class ForecastingEngine:
    """
    Time-Series Forecasting Engine providing trend projections with 95% confidence intervals.
    """

    @classmethod
    def forecast_metric(
        cls,
        df: pd.DataFrame,
        date_col: Optional[str],
        metric: str,
        periods_ahead: int = 12
    ) -> Dict[str, Any]:
        fallback_res = {
            "target_metric": metric,
            "forecast": [],
            "trend_direction": "Unknown",
            "confidence": 0.0,
            "model": "Linear Trend with 95% Expanding Prediction Intervals"
        }

        if metric not in df.columns or len(df) < 5:
            return fallback_res

        df_clean = df.copy()
        if date_col and date_col in df_clean.columns:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")
            df_clean = df_clean.dropna(subset=[date_col]).sort_values(by=date_col)
            
            # Determine appropriate resampling (Daily if short span, Monthly if long span)
            date_span_days = (df_clean[date_col].max() - df_clean[date_col].min()).days
            if date_span_days <= 60:
                grouped = df_clean.groupby(df_clean[date_col].dt.date)[metric].mean().reset_index()
            else:
                grouped = df_clean.groupby(df_clean[date_col].dt.to_period("M"))[metric].mean().reset_index()

            y_values = grouped[metric].values
            date_labels = [str(d) for d in grouped[date_col].values]
        else:
            y_values = df_clean[metric].dropna().values
            date_labels = [f"Period {i+1}" for i in range(len(y_values))]

        if len(y_values) < 3:
            return fallback_res

        n = len(y_values)
        x = np.arange(n)

        # Fit linear trend model
        slope, intercept, r_val, p_val, std_err = stats.linregress(x, y_values)
        r_squared = r_val ** 2

        # Calculate residual standard error for confidence bands
        y_hat = intercept + slope * x
        residuals = y_values - y_hat
        dof = max(n - 2, 1)
        residual_std = np.sqrt(np.sum(residuals ** 2) / dof)

        # Generate future periods
        forecast_items = []
        future_x = np.arange(n, n + periods_ahead)

        for idx, fx in enumerate(future_x):
            pred_y = intercept + slope * fx
            t_crit = 1.96
            sum_sq_diff = np.sum((x - np.mean(x)) ** 2)
            distance_factor = np.sqrt(1 + 1/n + (fx - np.mean(x))**2 / (sum_sq_diff if sum_sq_diff > 0 else 1.0))
            margin = t_crit * residual_std * distance_factor

            lower_bound = max(0.0, float(pred_y - margin))
            upper_bound = float(pred_y + margin)

            label = f"P+{idx+1}"
            if date_labels and len(date_labels) > 0:
                try:
                    last_val = pd.to_datetime(date_labels[-1])
                    label = str((last_val + pd.Timedelta(days=idx+1)).date())
                except Exception:
                    pass

            forecast_items.append({
                "period": label,
                "projected_value": round(float(pred_y), 2),
                "lower_bound_95": round(lower_bound, 2),
                "upper_bound_95": round(upper_bound, 2),
                "margin_of_error": round(float(margin), 2)
            })

        trend_direction = "Upward" if slope > 0 else ("Downward" if slope < 0 else "Flat")

        return {
            "target_metric": metric,
            "historical_periods": n,
            "slope": round(float(slope), 4),
            "r_squared": round(float(r_squared), 4),
            "p_value": round(float(p_val), 5),
            "trend_direction": trend_direction,
            "forecast": forecast_items,
            "model": "Linear Trend with 95% Expanding Prediction Intervals"
        }
