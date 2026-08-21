import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_full_investigation_pipeline():
    # Synthetic dataset with 2 months: June vs July
    dates = ["2026-06-01"] * 50 + ["2026-07-01"] * 50
    # June total revenue = 50 * 1000 = 50,000
    # July total revenue = 50 * 500 = 25,000 (Drop = -50%)
    revenues = [1000.0] * 50 + [500.0] * 50
    regions = ["West"] * 25 + ["East"] * 25 + ["West"] * 25 + ["East"] * 25
    delivery_days = [3.0] * 50 + [6.0] * 50 # Delivery days doubled in July

    df = pd.DataFrame({
        "order_date": dates,
        "revenue": revenues,
        "region": regions,
        "delivery_days": delivery_days
    })

    csv_buf = io.BytesIO()
    df.to_csv(csv_buf, index=False)
    csv_buf.seek(0)

    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("investigation_test.csv", csv_buf, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    inv_res = client.post(
        f"/api/datasets/{ds_id}/investigate",
        json={"metric": "revenue", "question": "Why did revenue decrease?"}
    )
    assert inv_res.status_code == 200
    data = inv_res.json()

    assert data["event"]["percentage_change"] == -50.0
    assert len(data["facts"]) >= 2
    assert len(data["potential_factors"]) >= 1
    assert data["confidence"] > 50.0
    assert data["ai_explanation"] is not None
