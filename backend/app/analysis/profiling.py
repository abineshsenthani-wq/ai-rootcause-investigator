import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.analysis.quality import DataQualityAnalyzer

class DataProfiler:
    """Performs comprehensive statistical profiling and column categorization."""

    METRIC_KEYWORDS = {
        "revenue", "sales", "profit", "price", "cost", "discount", "quantity", 
        "amount", "total", "spend", "score", "days", "orders", "customers", "units"
    }

    @classmethod
    def classify_columns(cls, df: pd.DataFrame) -> Dict[str, List[str]]:
        numerical_cols = []
        categorical_cols = []
        date_cols = []
        boolean_cols = []
        identifier_cols = []

        total_rows = len(df)

        for col in df.columns:
            col_lower = col.lower()
            series = df[col]

            # 1. Identifier detection
            if col_lower.endswith("_id") or col_lower in ["id", "order_id", "customer_id", "row_id", "uuid"]:
                identifier_cols.append(col)
                continue

            # 2. Date column detection
            if "date" in col_lower or "time" in col_lower:
                date_cols.append(col)
                continue

            # 3. Boolean column detection
            if pd.api.types.is_bool_dtype(series) or (series.dropna().isin([True, False, 0, 1]).all() and series.nunique() <= 2):
                boolean_cols.append(col)
                continue

            # 4. Numerical column detection
            if pd.api.types.is_numeric_dtype(series):
                # If metric keyword present or float or >5 unique values, treat as numerical
                is_metric_named = any(kw in col_lower for kw in cls.METRIC_KEYWORDS)
                if is_metric_named or pd.api.types.is_float_dtype(series) or series.nunique() > 5:
                    numerical_cols.append(col)
                else:
                    categorical_cols.append(col)
                continue

            # 5. Fallback categorical detection
            try:
                converted_dates = pd.to_datetime(series, errors="coerce", format="mixed")
                if converted_dates.notna().sum() / max(total_rows, 1) > 0.8:
                    date_cols.append(col)
                else:
                    categorical_cols.append(col)
            except Exception:
                categorical_cols.append(col)

        return {
            "numerical_columns": numerical_cols,
            "categorical_columns": categorical_cols,
            "date_columns": date_cols,
            "boolean_columns": boolean_cols,
            "identifier_columns": identifier_cols
        }

    @classmethod
    def profile_dataset(cls, df: pd.DataFrame) -> Dict[str, Any]:
        classification = cls.classify_columns(df)
        quality = DataQualityAnalyzer.evaluate_quality(df)
        total_rows = len(df)

        column_stats: Dict[str, Any] = {}

        # Profile Numerical Columns
        for col in classification["numerical_columns"]:
            series = df[col].dropna()
            missing_cnt = int(df[col].isna().sum())
            if len(series) > 0:
                column_stats[col] = {
                    "type": "numerical",
                    "missing_count": missing_cnt,
                    "missing_percentage": round((missing_cnt / total_rows) * 100, 2),
                    "unique_count": int(df[col].nunique()),
                    "mean": round(float(series.mean()), 4),
                    "median": round(float(series.median()), 4),
                    "min": round(float(series.min()), 4),
                    "max": round(float(series.max()), 4),
                    "std": round(float(series.std()), 4) if len(series) > 1 else 0.0
                }

        # Profile Categorical Columns
        for col in classification["categorical_columns"]:
            missing_cnt = int(df[col].isna().sum())
            value_counts = df[col].value_counts(dropna=True).head(5)
            top_categories = [
                {
                    "category": str(cat),
                    "frequency": int(freq),
                    "percentage": round((freq / total_rows) * 100, 2)
                }
                for cat, freq in value_counts.items()
            ]

            column_stats[col] = {
                "type": "categorical",
                "missing_count": missing_cnt,
                "missing_percentage": round((missing_cnt / total_rows) * 100, 2),
                "unique_count": int(df[col].nunique()),
                "top_categories": top_categories
            }

        # Profile Date Columns
        for col in classification["date_columns"]:
            missing_cnt = int(df[col].isna().sum())
            converted = pd.to_datetime(df[col], errors="coerce", format="mixed").dropna()
            if len(converted) > 0:
                min_d = converted.min()
                max_d = converted.max()
                days_span = (max_d - min_d).days
                column_stats[col] = {
                    "type": "date",
                    "missing_count": missing_cnt,
                    "min_date": str(min_d.date()),
                    "max_date": str(max_d.date()),
                    "time_span_days": days_span
                }

        return {
            "classification": classification,
            "quality": quality,
            "column_stats": column_stats
        }
