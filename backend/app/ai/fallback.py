from typing import Dict, Any

class DeterministicFallbackEngine:
    """Generates articulate evidence-grounded template explanations without needing external LLM API key."""

    @classmethod
    def generate_explanation(cls, evidence: Dict[str, Any]) -> str:
        event = evidence.get("event", {})
        metric = event.get("metric", "metric").replace("_", " ").title()
        pct_change = event.get("percentage_change", 0.0)
        p1 = event.get("start_period", "P1")
        p2 = event.get("end_period", "P2")

        facts = "\n".join([f"- {f}" for f in evidence.get("facts", [])])
        recommendations = "\n".join([f"- {r}" for r in evidence.get("recommendations", [])])

        factors_summary = []
        for factor in evidence.get("potential_factors", [])[:3]:
            factors_summary.append(
                f"- **{factor['factor_name']}**: Evidence Score {factor['evidence_score']}/100 ({factor['evidence_label']})"
            )
        factors_str = "\n".join(factors_summary) if factors_summary else "- No major slice contribution isolated."

        # Add Granger causality details if present
        causal_list = []
        for c in evidence.get("causal_inference", [])[:2]:
            if c.get("is_causal"):
                causal_list.append(f"- **{c['driver_variable']}**: Statistically significant lead variable (F={c['f_statistic']}, p={c['p_value']:.4f}, lag={c['best_lag_periods']} period(s)).")
        causal_str = "\n".join(causal_list) if causal_list else "- No statistically significant Granger causality leads isolated."

        # Add Correlation evidence
        corr_list = []
        for corr in evidence.get("evidence", [])[:3]:
            corr_list.append(
                f"- **{corr['correlated_variable']}**: r = {corr['pearson_correlation']:.2f} (p = {corr['p_value']:.4f}, 95% CI [{corr['confidence_interval_95'][0]:.2f}, {corr['confidence_interval_95'][1]:.2f}])"
            )
        corr_str = "\n".join(corr_list) if corr_list else "- No significant co-varying metrics detected."

        limitations_str = "\n".join([f"- {l}" for l in evidence.get("limitations", [])])

        return f"""### Executive Summary
Between **{p1}** and **{p2}**, target metric **{metric}** registered a **{pct_change:+.1f}%** shift. Multi-agent statistical decomposition evaluated segment contributions, co-varying operational indicators, and lead-lag Granger causality.

### Verified Facts
{facts}

### Statistical Co-variance & Correlations
{corr_str}

### Granger Causality Lead Drivers
{causal_str}

### Top Potential Contributing Slices
{factors_str}

### Actionable Recommendations
{recommendations}

### Statistical Limitations & Boundaries
{limitations_str}
"""
