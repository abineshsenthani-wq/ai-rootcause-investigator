import pandas as pd
from typing import Dict, Any, List
from app.ml.anomaly_detector import MultiMethodAnomalyDetector
from app.analysis.profiling import DataProfiler

class AnomalyAnalysisEngine:
    """Orchestrates multi-method anomaly detection across numerical columns."""

    @classmethod
    def run_anomaly_detection(cls, df: pd.DataFrame, metric: str = None) -> Dict[str, Any]:
        classification = DataProfiler.classify_columns(df)
        num_cols = classification["numerical_columns"]

        if not num_cols:
            return {"total_anomalies": 0, "anomalies": []}

        target_metric = metric if (metric and metric in num_cols) else num_cols[0]

        iqr_outliers = MultiMethodAnomalyDetector.detect_iqr_anomalies(df, target_metric)
        zscore_outliers = MultiMethodAnomalyDetector.detect_zscore_anomalies(df, target_metric)
        iforest_outliers = MultiMethodAnomalyDetector.detect_isolation_forest_anomalies(df, num_cols[:5])

        all_anomalies = iqr_outliers + zscore_outliers + iforest_outliers

        return {
            "metric": target_metric,
            "total_anomalies": len(all_anomalies),
            "summary_by_method": {
                "IQR": len(iqr_outliers),
                "Z-Score": len(zscore_outliers),
                "Isolation Forest": len(iforest_outliers)
            },
            "anomalies": all_anomalies[:50] # Top 50 anomalies for API payload
        }
