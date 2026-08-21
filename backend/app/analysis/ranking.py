from typing import Dict, Any, List

class RootCauseRankingEngine:
    """Calculates weighted multi-factor scores for potential root-cause drivers."""

    @classmethod
    def rank_factors(
        cls,
        contributions: List[Dict[str, Any]],
        correlations: List[Dict[str, Any]],
        anomalies_count: int
    ) -> List[Dict[str, Any]]:
        ranked_factors = []

        # 1. Process Segment Contributions
        for c in contributions[:5]:
            contrib_pct = min(float(c.get("contribution_percentage", 0.0)), 100.0)
            
            contrib_score = round(contrib_pct * 0.40, 2)
            corr_score = 15.0  # Baseline correlation score for segment slice
            temporal_score = 18.0
            anomaly_score = min(float(anomalies_count * 0.2), 10.0)
            coverage_score = 10.0

            total_score = round(contrib_score + corr_score + temporal_score + anomaly_score + coverage_score, 1)
            total_score = min(total_score, 100.0)

            evidence_label = "HIGH EVIDENCE" if total_score >= 70.0 else ("MODERATE EVIDENCE" if total_score >= 50.0 else "LOW EVIDENCE")

            factor_name = f"{c['dimension'].replace('_', ' ').title()}: {c['segment']}"
            ranked_factors.append({
                "factor_name": factor_name,
                "dimension": c["dimension"],
                "segment": c["segment"],
                "metric_change_pct": c["percentage_change"],
                "contribution_pct": c["contribution_percentage"],
                "evidence_score": total_score,
                "score_breakdown": {
                    "contribution_score": contrib_score,
                    "correlation_score": corr_score,
                    "temporal_alignment_score": temporal_score,
                    "anomaly_strength_score": anomaly_score,
                    "data_coverage_score": coverage_score
                },
                "evidence_label": evidence_label
            })

        # 2. Process Numerical Variable Correlations
        for corr in correlations[:3]:
            abs_corr = abs(float(corr.get("pearson_correlation", 0.0)))
            corr_component = round(abs_corr * 20.0, 2)
            contrib_component = 30.0
            temporal_component = 16.0
            anomaly_component = 8.0
            coverage_component = 10.0

            total_score = round(contrib_component + corr_component + temporal_component + anomaly_component + coverage_component, 1)
            total_score = min(total_score, 100.0)

            evidence_label = "HIGH EVIDENCE" if total_score >= 70.0 else ("MODERATE EVIDENCE" if total_score >= 50.0 else "LOW EVIDENCE")

            factor_name = f"Co-varying Metric: {corr['correlated_variable'].replace('_', ' ').title()}"
            ranked_factors.append({
                "factor_name": factor_name,
                "dimension": "numerical_correlation",
                "segment": corr["correlated_variable"],
                "metric_change_pct": 0.0,
                "contribution_pct": 0.0,
                "evidence_score": total_score,
                "score_breakdown": {
                    "contribution_score": contrib_component,
                    "correlation_score": corr_component,
                    "temporal_alignment_score": temporal_component,
                    "anomaly_strength_score": anomaly_component,
                    "data_coverage_score": coverage_component
                },
                "evidence_label": evidence_label
            })

        # Sort by total evidence score descending
        ranked_factors.sort(key=lambda x: x["evidence_score"], reverse=True)
        return ranked_factors
