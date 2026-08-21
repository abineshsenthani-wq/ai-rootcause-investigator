import pandas as pd
from typing import Dict, Any, List
from app.analysis.profiling import DataProfiler
from app.analysis.trends import TimeTrendEngine
from app.analysis.events import EventDetectionEngine
from app.analysis.anomalies import AnomalyAnalysisEngine
from app.analysis.segments import SegmentAnalysisEngine
from app.analysis.contributions import ContributionAnalysisEngine
from app.analysis.correlations import CorrelationAnalysisEngine
from app.analysis.ranking import RootCauseRankingEngine
from app.analysis.causal import GrangerCausalityEngine
from app.analysis.forecasting import ForecastingEngine
from app.ai.agents import DetectionAgent, CausalInferenceAgent, SynthesisAgent

class InvestigationEngine:
    """End-to-end multi-agent investigation pipeline orchestrating profiling, trends, events, anomalies, segments, Granger causality, forecasting, and RAG vector memory synthesis."""

    @classmethod
    def investigate(
        cls,
        df: pd.DataFrame,
        target_metric: str = None,
        start_period: str = None,
        end_period: str = None,
        user_question: str = None
    ) -> Dict[str, Any]:
        # 1. Profile Dataset
        profile = DataProfiler.profile_dataset(df)
        classification = profile["classification"]

        metric = target_metric or (classification["numerical_columns"][0] if classification["numerical_columns"] else "revenue")
        date_col = classification["date_columns"][0] if classification["date_columns"] else None

        # 2. Trend & Event Analysis
        trend_data = {}
        events = []
        if date_col:
            trend_data = TimeTrendEngine.calculate_trend(df, date_col, metric)
            events = EventDetectionEngine.detect_events(df, date_col, metric)

        summary_change = trend_data.get("summary", {})
        pct_change = summary_change.get("percentage_change", 0.0)

        # 3. Multi-method Anomaly Detection
        anomalies_data = AnomalyAnalysisEngine.run_anomaly_detection(df, metric=metric)

        # 4. Segment & Contribution Analysis
        dim_cols = classification["categorical_columns"]
        p1 = start_period or summary_change.get("previous_period", "P1")
        p2 = end_period or summary_change.get("current_period", "P2")

        segment_results = {}
        contributions = []
        if date_col and dim_cols:
            segment_results = SegmentAnalysisEngine.analyze_segments(df, date_col, metric, dim_cols, str(p1), str(p2))
            contributions = ContributionAnalysisEngine.calculate_contributions(segment_results, pct_change)

        # 5. Statistical Correlations & P-Values
        correlations = CorrelationAnalysisEngine.calculate_correlations(df, metric, classification["numerical_columns"])

        # 6. Granger Causality Lead-Lag Tests
        causal_results = GrangerCausalityEngine.test_causality(df, date_col, metric, classification["numerical_columns"])

        # 7. Time-Series 30-Day Forecast
        forecast_data = ForecastingEngine.forecast_metric(df, date_col, metric, periods_ahead=12)

        # 8. Factor Ranking
        potential_factors = RootCauseRankingEngine.rank_factors(
            contributions=contributions,
            correlations=correlations,
            anomalies_count=anomalies_data.get("total_anomalies", 0)
        )

        # 9. Multi-Agent Analysis Execution
        det_agent_res = DetectionAgent.analyze(trend_data, anomalies_data)
        causal_agent_res = CausalInferenceAgent.analyze(contributions, correlations, causal_results)

        # 10. Formulate Facts, Hypotheses, Recommendations
        facts = [
            f"{metric.replace('_', ' ').title()} changed by {pct_change:+.1f}% across comparison window ({p1} → {p2}).",
            f"A total of {anomalies_data.get('total_anomalies', 0)} transaction anomalies were detected via IQR, Z-Score, and Isolation Forest."
        ]
        if contributions:
            top_c = contributions[0]
            facts.append(
                f"The shift was heavily concentrated in {top_c['dimension'].replace('_', ' ').title()} '{top_c['segment']}', "
                f"accounting for {top_c['contribution_percentage']}% of total change."
            )
        if causal_results and causal_results[0].get("is_causal"):
            top_causal = causal_results[0]
            facts.append(
                f"Granger causality testing confirms '{top_causal['driver_variable']}' as a statistically significant causal lead "
                f"(F={top_causal['f_statistic']}, p={top_causal['p_value']:.4f}, lag={top_causal['best_lag_periods']})."
            )

        synth_agent_res = SynthesisAgent.synthesize(metric, det_agent_res, causal_agent_res, facts)

        hypotheses = []
        for factor in potential_factors[:3]:
            hypotheses.append({
                "factor": factor["factor_name"],
                "evidence_score": factor["evidence_score"],
                "evidence_label": factor["evidence_label"],
                "statement": f"{factor['factor_name']} shows a strong statistical association (Score: {factor['evidence_score']}/100) with the observed shift in {metric}."
            })

        recommendations = []
        if contributions:
            top_dim = contributions[0]["dimension"]
            top_seg = contributions[0]["segment"]
            recommendations.append(f"Audit operational performance, supply chain, and inventory fulfillment in {top_dim.replace('_', ' ')} '{top_seg}'.")
        if correlations:
            top_corr_var = correlations[0]["correlated_variable"]
            recommendations.append(f"Investigate recent SLA or policy changes affecting '{top_corr_var.replace('_', ' ')}'.")
        if causal_results and causal_results[0].get("is_causal"):
            recommendations.append(f"Prioritize intervention on lead variable '{causal_results[0]['driver_variable']}' to prevent downstream metric decline.")
        recommendations.append("Conduct controlled counterfactual simulations via the What-If Engine to model recovery scenarios.")

        limitations = [
            "Granger causality proves temporal precedence, but external unobserved confounding variables may still exist.",
            "External macro market factors (competitor pricing, inflation, seasonal shifts) are not captured in the uploaded dataset."
        ]

        return {
            "event": events[0] if events else {
                "metric": metric,
                "event_type": "METRIC_SHIFT",
                "start_period": str(p1),
                "end_period": str(p2),
                "previous_value": summary_change.get("previous_value", 0.0),
                "current_value": summary_change.get("current_value", 0.0),
                "absolute_change": summary_change.get("absolute_change", 0.0),
                "percentage_change": pct_change,
                "severity": EventDetectionEngine.calculate_severity(pct_change)
            },
            "summary": f"{metric.replace('_', ' ').title()} changed by {pct_change:+.1f}% between {p1} and {p2}.",
            "facts": facts,
            "potential_factors": potential_factors,
            "evidence": correlations,
            "causal_inference": causal_results,
            "forecast": forecast_data,
            "similar_incidents": synth_agent_res.get("rag_similar_incidents", []),
            "anomalies": anomalies_data.get("anomalies", []),
            "hypotheses": hypotheses,
            "recommendations": recommendations,
            "confidence": synth_agent_res.get("confidence_score", 85.0),
            "limitations": limitations
        }
