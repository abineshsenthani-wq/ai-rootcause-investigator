import pandas as pd
import numpy as np
from app.analysis.causal import GrangerCausalityEngine

def test_granger_causality():
    np.random.seed(42)
    n = 50
    dates = pd.date_range("2026-01-01", periods=n, freq="D")
    driver = np.random.randn(n).cumsum()
    # Target lags driver by 1 day
    target = np.roll(driver, 1) * 2 + np.random.randn(n) * 0.1

    df = pd.DataFrame({"date": dates, "revenue": target, "delivery_days": driver})
    results = GrangerCausalityEngine.test_causality(df, "date", "revenue", ["delivery_days"])

    assert len(results) > 0
    assert results[0]["driver_variable"] == "delivery_days"
    assert "p_value" in results[0]
