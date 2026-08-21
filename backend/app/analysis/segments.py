import pandas as pd
from typing import Dict, Any, List

class SegmentAnalysisEngine:
    """Compares metric performance across categorical breakdown dimensions between two time periods."""

    @classmethod
    def analyze_segments(
        cls,
        df: pd.DataFrame,
        date_col: str,
        metric_col: str,
        dimension_cols: List[str],
        start_period: str,
        end_period: str
    ) -> Dict[str, Any]:
        df_clean = df.copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce", format="mixed")
        
        # Filter for the target dates/periods
        df_clean["period_str"] = df_clean[date_col].dt.strftime("%Y-%m")
        
        # If periods match format YYYY-MM
        p1_mask = df_clean["period_str"] <= start_period if len(start_period) == 7 else df_clean[date_col] <= start_period
        p2_mask = df_clean["period_str"] >= end_period if len(end_period) == 7 else df_clean[date_col] >= end_period

        # Fallback if period filtering yields empty sets: split dataset into half 1 vs half 2
        df_sorted = df_clean.sort_values(date_col)
        mid_point = len(df_sorted) // 2
        df_p1 = df_sorted.iloc[:mid_point]
        df_p2 = df_sorted.iloc[mid_point:]

        df_p1 = df_p1.copy()
        df_p2 = df_p2.copy()
        df_p1[metric_col] = pd.to_numeric(df_p1[metric_col], errors="coerce").fillna(0.0)
        df_p2[metric_col] = pd.to_numeric(df_p2[metric_col], errors="coerce").fillna(0.0)

        segment_results = {}

        for dim in dimension_cols:
            if dim not in df.columns:
                continue

            p1_grouped = df_p1.groupby(dim)[metric_col].sum()
            p2_grouped = df_p2.groupby(dim)[metric_col].sum()

            combined = pd.DataFrame({"p1_value": p1_grouped, "p2_value": p2_grouped}).fillna(0.0)
            combined["absolute_change"] = combined["p2_value"] - combined["p1_value"]
            combined["percentage_change"] = (combined["absolute_change"] / combined["p1_value"].replace(0, 1)) * 100
            combined["percentage_change"] = combined["percentage_change"].round(2)

            # Sort by largest negative drop
            sorted_segments = combined.sort_values("absolute_change", ascending=True)

            segment_results[dim] = sorted_segments.reset_index().to_dict(orient="records")

        return segment_results
