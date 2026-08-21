import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, List

class MultiMethodAnomalyDetector:
    """Multi-method statistical and machine learning anomaly detection engine optimized for high scale."""

    @staticmethod
    def detect_iqr_anomalies(df: pd.DataFrame, metric_col: str) -> List[Dict[str, Any]]:
        if metric_col not in df.columns:
            return []
        series = df[metric_col].dropna()
        if len(series) < 4:
            return []

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_fence = q1 - (1.5 * iqr)
        upper_fence = q3 + (1.5 * iqr)

        mask = (series < lower_fence) | (series > upper_fence)
        outlier_series = series[mask].head(50)

        outliers = []
        for idx, val in outlier_series.items():
            dist = max(abs(val - lower_fence), abs(val - upper_fence)) / max(iqr, 1e-5)
            severity = "HIGH" if dist > 3.0 else ("MEDIUM" if dist > 1.5 else "LOW")
            outliers.append({
                "row_id": int(idx),
                "metric": metric_col,
                "value": round(float(val), 2),
                "expected_range": f"{round(lower_fence, 2)} to {round(upper_fence, 2)}",
                "anomaly_score": round(float(dist), 2),
                "method": "IQR",
                "severity": severity
            })
        return outliers

    @staticmethod
    def detect_zscore_anomalies(df: pd.DataFrame, metric_col: str, z_threshold: float = 3.0) -> List[Dict[str, Any]]:
        if metric_col not in df.columns:
            return []
        series = df[metric_col].dropna()
        if len(series) < 4 or series.std() == 0:
            return []

        mean_val = series.mean()
        std_val = series.std()

        z_scores = (series - mean_val) / std_val
        mask = z_scores.abs() >= z_threshold
        outlier_z = z_scores[mask].head(50)

        outliers = []
        for idx, z in outlier_z.items():
            val = series.loc[idx]
            severity = "CRITICAL" if abs(z) >= 4.0 else ("HIGH" if abs(z) >= 3.5 else "MEDIUM")
            outliers.append({
                "row_id": int(idx),
                "metric": metric_col,
                "value": round(float(val), 2),
                "expected_range": f"{round(mean_val - z_threshold*std_val, 2)} to {round(mean_val + z_threshold*std_val, 2)}",
                "anomaly_score": round(float(abs(z)), 2),
                "method": "Z-Score",
                "severity": severity
            })
        return outliers

    @staticmethod
    def detect_isolation_forest_anomalies(df: pd.DataFrame, numerical_cols: List[str]) -> List[Dict[str, Any]]:
        valid_cols = [c for c in numerical_cols if c in df.columns]
        if not valid_cols:
            return []

        df_num = df[valid_cols].dropna()
        if len(df_num) < 10:
            return []

        # Sampling for ultra-fast training and prediction on massive datasets
        fit_sample = df_num.sample(n=min(len(df_num), 10000), random_state=42)

        model = IsolationForest(contamination=0.01, random_state=42, n_jobs=-1)
        model.fit(fit_sample)

        eval_sample = df_num if len(df_num) <= 50000 else df_num.head(50000)
        scores = model.decision_function(eval_sample)
        predictions = model.predict(eval_sample)

        outlier_indices = np.where(predictions == -1)[0][:50]
        primary_metric = valid_cols[0]

        outliers = []
        for i in outlier_indices:
            idx = eval_sample.index[i]
            row = eval_sample.iloc[i]
            score = round(float(-scores[i]), 4)
            severity = "CRITICAL" if score > 0.15 else ("HIGH" if score > 0.08 else "MEDIUM")
            outliers.append({
                "row_id": int(idx),
                "metric": primary_metric,
                "value": round(float(row[primary_metric]), 2),
                "expected_range": "Isolation Forest Decision Boundary",
                "anomaly_score": score,
                "method": "Isolation Forest",
                "severity": severity
            })

        return outliers
