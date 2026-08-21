import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine
from app.analysis.profiling import DataProfiler

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_data_profiler_classification():
    df = pd.DataFrame({
        "order_id": [101, 102, 103, 104, 105],
        "order_date": ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05"],
        "revenue": [100.5, 200.0, 150.75, 300.0, 250.0],
        "region": ["West", "East", "West", "North", "West"],
        "is_expedited": [True, False, True, False, True]
    })

    result = DataProfiler.profile_dataset(df)
    classification = result["classification"]

    assert "order_id" in classification["identifier_columns"]
    assert "order_date" in classification["date_columns"]
    assert "revenue" in classification["numerical_columns"]
    assert "region" in classification["categorical_columns"]
    assert "is_expedited" in classification["boolean_columns"]

def test_profile_api_endpoint():
    csv_data = (
        "order_id,order_date,revenue,region\n"
        "1,2026-06-01,500,West\n"
        "2,2026-06-02,600,East\n"
        "3,2026-06-03,450,West\n"
    )
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("profiling_test.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    profile_res = client.get(f"/api/datasets/{ds_id}/profile")
    assert profile_res.status_code == 200
    data = profile_res.json()

    assert data["dataset_id"] == ds_id
    assert "revenue" in data["column_stats"]
    assert data["column_stats"]["revenue"]["type"] == "numerical"
    assert data["column_stats"]["revenue"]["mean"] == 516.6667
    assert data["quality"]["missing_cells"] == 0
