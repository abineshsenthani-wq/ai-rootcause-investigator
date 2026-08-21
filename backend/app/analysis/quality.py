import pandas as pd
from typing import Dict, Any

class DataQualityAnalyzer:
    """Analyzes missing values, duplicate rows, and constant column issues."""
    
    @staticmethod
    def evaluate_quality(df: pd.DataFrame) -> Dict[str, Any]:
        total_rows = len(df)
        total_cells = df.size
        missing_cells = int(df.isna().sum().sum())
        missing_percentage = float((missing_cells / total_cells * 100)) if total_cells > 0 else 0.0

        duplicate_rows = int(df.duplicated().sum())

        constant_columns = [col for col in df.columns if df[col].nunique(dropna=True) <= 1]
        empty_columns = [col for col in df.columns if df[col].isna().all()]

        return {
            "total_rows": total_rows,
            "total_columns": len(df.columns),
            "missing_cells": missing_cells,
            "missing_percentage": round(missing_percentage, 2),
            "duplicate_rows": duplicate_rows,
            "constant_columns": constant_columns,
            "empty_columns": empty_columns,
            "is_clean": (missing_percentage < 5.0 and len(empty_columns) == 0)
        }
