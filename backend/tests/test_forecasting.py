import pandas as pd
import numpy as np
from app.analysis.forecasting import ForecastingEngine

def test_forecasting_engine():
    np.random.seed(42)
    n = 30
    dates = pd.date_range("2026-01-01", periods=n, freq="D")
    y = np.linspace(100, 200, n) + np.random.randn(n) * 2

    df = pd.DataFrame({"date": dates, "revenue": y})
    result = ForecastingEngine.forecast_metric(df, "date", "revenue", periods_ahead=5)

    assert result["target_metric"] == "revenue"
    assert len(result["forecast"]) == 5
    assert "lower_bound_95" in result["forecast"][0]
    assert "upper_bound_95" in result["forecast"][0]
