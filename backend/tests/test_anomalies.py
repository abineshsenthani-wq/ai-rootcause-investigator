import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine
from app.ml.anomaly_detector import MultiMethodAnomalyDetector

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_iqr_and_zscore_anomalies():
    # 20 normal values around 100, 1 extreme outlier 5000
    values = [100.0 + (i % 5) for i in range(20)] + [5000.0]
    df = pd.DataFrame({"revenue": values})

    iqr_res = MultiMethodAnomalyDetector.detect_iqr_anomalies(df, "revenue")
    z_res = MultiMethodAnomalyDetector.detect_zscore_anomalies(df, "revenue")

    assert len(iqr_res) >= 1
    assert iqr_res[0]["value"] == 5000.0
    assert len(z_res) >= 1
    assert z_res[0]["value"] == 5000.0

def test_anomalies_api_endpoint():
    csv_data = "revenue,quantity\n" + "\n".join([f"100,{i}" for i in range(30)]) + "\n95000,500\n"
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("anomaly_test.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    anom_res = client.get(f"/api/datasets/{ds_id}/anomalies")
    assert anom_res.status_code == 200
    data = anom_res.json()

    assert data["total_anomalies"] >= 1
    assert "IQR" in data["summary_by_method"]
