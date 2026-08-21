import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime

class TimeTrendEngine:
    """Analyzes metric time-series trends, period-over-period changes, and rolling stats."""

    @staticmethod
    def auto_determine_granularity(df: pd.DataFrame, date_col: str) -> str:
        """Determines optimal aggregation frequency ('D', 'W', 'M', 'Q', 'Y') based on date span and unique months."""
        series = pd.to_datetime(df[date_col], errors="coerce", format="mixed").dropna()
        if len(series) == 0:
            return "M"
        
        unique_months = series.dt.to_period("M").nunique()
        span_days = (series.max() - series.min()).days

        if unique_months > 1 and span_days >= 28:
            return "M"      # Monthly
        elif span_days <= 14:
            return "D"      # Daily
        elif span_days <= 90:
            return "W"      # Weekly
        elif span_days <= 730:
            return "M"      # Monthly
        elif span_days <= 1825:
            return "Q"      # Quarterly
        else:
            return "Y"      # Yearly

    @classmethod
    def calculate_trend(
        cls,
        df: pd.DataFrame,
        date_col: str,
        metric_col: str,
        granularity: Optional[str] = None
    ) -> Dict[str, Any]:
        """Aggregates metric values by date granularity and computes percentage change, rolling average, and spikes/drops."""
        df_clean = df.copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce", format="mixed")
        df_clean = df_clean.dropna(subset=[date_col, metric_col])

        if df_clean.empty:
            return {
                "metric": metric_col,
                "date_column": date_col,
                "granularity": granularity or "M",
                "trend_points": [],
                "summary": {}
            }

        if not granularity:
            granularity = cls.auto_determine_granularity(df_clean, date_col)

        # Set date index and resample
        df_clean = df_clean.set_index(date_col).sort_index()
        
        freq_map = {
            "D": "1D",
            "W": "1W",
            "M": "1ME",
            "Q": "1QE",
            "Y": "1YE"
        }
        resample_rule = freq_map.get(granularity.upper(), "1ME")

        resampled = df_clean[metric_col].resample(resample_rule).sum().reset_index()
        # Drop periods with zero sums created by sparse resampling gap padding if they are not in original range
        resampled = resampled[resampled[metric_col] > 0].reset_index(drop=True)
        resampled[date_col] = resampled[date_col].dt.strftime("%Y-%m-%d")

        # Calculate Period-over-Period shifts
        resampled["previous_value"] = resampled[metric_col].shift(1)
        resampled["absolute_change"] = resampled[metric_col] - resampled["previous_value"]
        resampled["percentage_change"] = np.where(
            resampled["previous_value"] > 0,
            (resampled["absolute_change"] / resampled["previous_value"]) * 100,
            0.0
        )
        resampled["percentage_change"] = resampled["percentage_change"].round(2)

        # Calculate 3-period rolling average
        resampled["rolling_avg_3"] = resampled[metric_col].rolling(window=3, min_periods=1).mean().round(2)

        trend_points = resampled.to_dict(orient="records")

        summary = {}
        if len(resampled) >= 2:
            prev_row = resampled.iloc[-2]
            curr_row = resampled.iloc[-1]
            summary = {
                "previous_period": prev_row[date_col],
                "current_period": curr_row[date_col],
                "previous_value": float(prev_row[metric_col]),
                "current_value": float(curr_row[metric_col]),
                "absolute_change": float(curr_row["absolute_change"]),
                "percentage_change": float(curr_row["percentage_change"])
            }

        return {
            "metric": metric_col,
            "date_column": date_col,
            "granularity": granularity,
            "trend_points": trend_points,
            "summary": summary
        }
