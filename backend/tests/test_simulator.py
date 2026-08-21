import pandas as pd
import numpy as np
from app.analysis.simulator import WhatIfSimulator

def test_what_if_simulator():
    np.random.seed(42)
    n = 40
    delivery_days = np.random.uniform(1, 10, n)
    revenue = 1000 - 50 * delivery_days + np.random.randn(n) * 5

    df = pd.DataFrame({"revenue": revenue, "delivery_days": delivery_days})
    result = WhatIfSimulator.simulate_counterfactual(df, "revenue", {"delivery_days": -2.0})

    assert result["target_metric"] == "revenue"
    assert "simulated_mean" in result
    assert len(result["variable_impacts"]) == 1
    assert result["variable_impacts"][0]["user_adjustment_delta"] == -2.0
