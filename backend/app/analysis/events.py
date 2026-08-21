from typing import Dict, Any, List
import pandas as pd
from app.analysis.trends import TimeTrendEngine

class EventDetectionEngine:
    """Detects unusual metric drops or spikes and calculates event severity."""

    @staticmethod
    def calculate_severity(percentage_change: float) -> str:
        abs_change = abs(percentage_change)
        if abs_change >= 30.0:
            return "CRITICAL"
        elif abs_change >= 20.0:
            return "HIGH"
        elif abs_change >= 10.0:
            return "MEDIUM"
        elif abs_change >= 5.0:
            return "LOW"
        else:
            return "NORMAL"

    @classmethod
    def detect_events(
        cls,
        df: pd.DataFrame,
        date_col: str,
        metric_col: str,
        granularity: str = None
    ) -> List[Dict[str, Any]]:
        trend_result = TimeTrendEngine.calculate_trend(df, date_col, metric_col, granularity)
        trend_points = trend_result["trend_points"]

        events = []
        for i in range(1, len(trend_points)):
            prev_pt = trend_points[i - 1]
            curr_pt = trend_points[i]

            pct_change = curr_pt.get("percentage_change", 0.0)
            severity = cls.calculate_severity(pct_change)

            if severity != "NORMAL":
                event_type = "METRIC_DROP" if pct_change < 0 else "METRIC_SPIKE"
                events.append({
                    "metric": metric_col,
                    "event_type": event_type,
                    "start_period": prev_pt[date_col],
                    "end_period": curr_pt[date_col],
                    "previous_value": float(prev_pt[metric_col]),
                    "current_value": float(curr_pt[metric_col]),
                    "absolute_change": float(curr_pt["absolute_change"]),
                    "percentage_change": float(pct_change),
                    "severity": severity
                })

        return events
