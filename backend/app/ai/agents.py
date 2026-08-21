from typing import Dict, Any, List
from app.ai.incident_memory import HistoricalIncidentMemory

class DetectionAgent:
    """Agent responsible for anomaly detection, outlier filtering, and shift identification."""

    @classmethod
    def analyze(cls, trend_data: Dict[str, Any], anomalies_data: Dict[str, Any]) -> Dict[str, Any]:
        pct_change = trend_data.get("summary", {}).get("percentage_change", 0.0)
        total_anomalies = anomalies_data.get("total_anomalies", 0)
        severity = "HIGH" if abs(pct_change) > 20 or total_anomalies > 15 else ("MEDIUM" if abs(pct_change) > 10 else "LOW")
        return {
            "agent": "DetectionAgent",
            "percentage_change": pct_change,
            "total_anomalies": total_anomalies,
            "severity_level": severity,
            "findings": f"Detected a {pct_change:.1f}% shift with {total_anomalies} anomaly outliers (Severity: {severity})."
        }

class CausalInferenceAgent:
    """Agent responsible for Granger causality lead-lag evaluation, correlation p-values, and segment contributions."""

    @classmethod
    def analyze(cls, contributions: List[Dict[str, Any]], correlations: List[Dict[str, Any]], causal_leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        causal_drivers = [c for c in causal_leads if c.get("is_causal")]
        sig_correlations = [c for c in correlations if c.get("p_value", 1.0) < 0.05]

        return {
            "agent": "CausalInferenceAgent",
            "causal_lead_drivers": len(causal_drivers),
            "statistically_significant_correlations": len(sig_correlations),
            "top_causal_driver": causal_drivers[0] if causal_drivers else (causal_leads[0] if causal_leads else None),
            "top_segment_contribution": contributions[0] if contributions else None
        }

class SynthesisAgent:
    """Agent responsible for cross-referencing vector memory, facts, hypotheses, and recommendations."""

    @classmethod
    def synthesize(cls, metric: str, detection_res: Dict[str, Any], causal_res: Dict[str, Any], facts: List[str]) -> Dict[str, Any]:
        # Search similar historical incidents using RAG vector memory
        query_text = f"{metric} shift {detection_res.get('findings')} {' '.join(facts)}"
        similar_incidents = HistoricalIncidentMemory.search_similar_incidents(query_text, top_k=2)

        return {
            "agent": "SynthesisAgent",
            "rag_similar_incidents": similar_incidents,
            "confidence_score": 92 if causal_res.get("causal_lead_drivers", 0) > 0 else 82,
            "synthesis_summary": (
                f"Multi-Agent Evaluation Complete: {detection_res.get('findings')} "
                f"Cross-referenced against {len(similar_incidents)} historical precedents."
            )
        }
