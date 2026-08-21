import pandas as pd
from typing import Dict, Any, List

class ContributionAnalysisEngine:
    """Calculates mathematical percentage contribution of individual dimension slices to overall metric decline/increase."""

    @classmethod
    def calculate_contributions(
        cls,
        segment_results: Dict[str, List[Dict[str, Any]]],
        total_metric_change: float
    ) -> List[Dict[str, Any]]:
        """Formula: Contribution % = (Segment Metric Decline / Total Metric Decline) * 100%"""
        contributions = []

        if total_metric_change == 0:
            return contributions

        for dim, rows in segment_results.items():
            for row in rows:
                seg_name = str(row.get(dim, "Unknown"))
                abs_change = float(row.get("absolute_change", 0.0))
                pct_change = float(row.get("percentage_change", 0.0))

                # If overall metric dropped, evaluate segments that also dropped
                if total_metric_change < 0 and abs_change < 0:
                    contrib_pct = round((abs_change / total_metric_change) * 100, 2)
                    contributions.append({
                        "dimension": dim,
                        "segment": seg_name,
                        "previous_value": float(row.get("p1_value", 0.0)),
                        "current_value": float(row.get("p2_value", 0.0)),
                        "absolute_change": abs_change,
                        "percentage_change": pct_change,
                        "contribution_percentage": contrib_pct
                    })
                elif total_metric_change > 0 and abs_change > 0:
                    contrib_pct = round((abs_change / total_metric_change) * 100, 2)
                    contributions.append({
                        "dimension": dim,
                        "segment": seg_name,
                        "previous_value": float(row.get("p1_value", 0.0)),
                        "current_value": float(row.get("p2_value", 0.0)),
                        "absolute_change": abs_change,
                        "percentage_change": pct_change,
                        "contribution_percentage": contrib_pct
                    })

        # Sort by highest contribution percentage
        contributions.sort(key=lambda x: x["contribution_percentage"], reverse=True)
        return contributions
