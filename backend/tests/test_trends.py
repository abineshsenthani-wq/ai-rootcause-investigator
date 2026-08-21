import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine
from app.analysis.trends import TimeTrendEngine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_time_trend_engine():
    df = pd.DataFrame({
        "order_date": ["2026-06-01", "2026-06-15", "2026-07-01", "2026-07-15"],
        "revenue": [1000, 1000, 700, 800]
    })

    result = TimeTrendEngine.calculate_trend(df, date_col="order_date", metric_col="revenue", granularity="M")
    assert result["metric"] == "revenue"
    assert result["granularity"] == "M"
    assert len(result["trend_points"]) == 2

    # June = 2000, July = 1500 -> Change = (1500 - 2000)/2000 = -25%
    june_pt = result["trend_points"][0]
    july_pt = result["trend_points"][1]

    assert june_pt["revenue"] == 2000
    assert july_pt["revenue"] == 1500
    assert july_pt["percentage_change"] == -25.0

def test_trends_api_endpoint():
    csv_data = (
        "order_date,revenue\n"
        "2026-06-01,1000\n"
        "2026-06-20,1000\n"
        "2026-07-01,500\n"
        "2026-07-20,500\n"
    )
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("trend_test.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    trend_res = client.get(f"/api/datasets/{ds_id}/trends?granularity=M")
    assert trend_res.status_code == 200
    data = trend_res.json()

    assert data["metric"] == "revenue"
    assert data["granularity"] == "M"
    assert len(data["trend_points"]) == 2
    assert data["summary"]["percentage_change"] == -50.0
