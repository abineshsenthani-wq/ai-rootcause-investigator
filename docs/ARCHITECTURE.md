# AI ROOT-CAUSE INVESTIGATOR: System Architecture Document

## 1. Executive Pipeline Architecture

```
DATA INGESTION (CSV/XLSX)
        ↓
DATA PROFILING & QUALITY CHECK (Pandas, SciPy)
        ↓
TIME TREND ENGINE (Auto-Granularity: D, W, M, Q, Y)
        ↓
EVENT DETECTION (Severity Scoring: LOW, MEDIUM, HIGH, CRITICAL)
        ↓
MULTI-METHOD ANOMALY ENGINE (Tukey IQR, Z-Score, Isolation Forest ML)
        ↓
SEGMENT ANALYSIS ENGINE (Dimensional Drill-Down)
        ↓
CORRELATION ANALYSIS ENGINE (Pearson & Spearman Rank Monotonic)
        ↓
MATHEMATICAL CONTRIBUTION ENGINE (Segment Drop / Total Drop * 100%)
        ↓
ROOT-CAUSE MULTI-FACTOR RANKING ENGINE (Weighted Score out of 100)
        ↓
STRUCTURED EVIDENCE JSON (Facts, Hypotheses, Factors, Recommendations)
        ↓
LLM EXPLANATION LAYER (OpenAI / Anthropic / Fallback Abstraction)
        ↓
REACT FRONTEND WORKSPACE & PDF REPORT (Recharts, Evidence Graph)
```

## 2. Mathematical & Machine Learning Algorithms

### 2.1 Multi-Method Anomaly Detection
1. **IQR (Interquartile Range)**:
   $$\text{IQR} = Q_3 - Q_1$$
   $$\text{Fences}: [Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$$
2. **Z-Score Normalization**:
   $$Z = \frac{X - \mu}{\sigma}, \quad \text{Flagged if } |Z| \ge 3.0$$
3. **Isolation Forest (Scikit-Learn)**:
   - Unsupervised tree isolation with contamination threshold $0.01$.

### 2.2 Mathematical Segment Contribution
$$\text{Contribution \%} = \left( \frac{\Delta \text{Segment Metric}}{\Delta \text{Total Metric}} \right) \times 100\%$$

### 2.3 Root-Cause Ranking Score Formula
$$\text{Total Evidence Score} = \text{Contrib (40\%)} + \text{Corr (20\%)} + \text{Temporal (20\%)} + \text{Anomaly (10\%)} + \text{Coverage (10\%)}$$
- **Score $\ge 70$**: `HIGH EVIDENCE`
- **Score $50 - 69$**: `MODERATE EVIDENCE`
- **Score $< 50$**: `LOW EVIDENCE`

## 3. Grounded LLM Prompt Abstraction
The system guarantees zero hallucinated figures by passing Python-computed JSON evidence directly into the LLM system prompt. If no API key is provided, a deterministic template engine yields complete executive explanations offline.
