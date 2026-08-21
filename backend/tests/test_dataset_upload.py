import pytest
import io
import os
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    # Ensure all tables exist before every test
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_upload_valid_csv():
    csv_data = "order_date,revenue,region,quantity\n2026-06-01,1000,West,5\n2026-07-01,800,East,4\n"
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))

    response = client.post(
        "/api/datasets/upload",
        files={"file": ("test_business_data.csv", file_bytes, "text/csv")}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test_business_data.csv"
    assert data["row_count"] == 2
    assert data["column_count"] == 4
    assert data["primary_metric"] == "revenue"
    assert data["date_column"] == "order_date"

def test_upload_invalid_extension():
    file_bytes = io.BytesIO(b"dummy data")
    response = client.post(
        "/api/datasets/upload",
        files={"file": ("test.pdf", file_bytes, "application/pdf")}
    )
    assert response.status_code == 400
    assert "Unsupported file extension" in response.json()["detail"]

def test_upload_empty_file():
    file_bytes = io.BytesIO(b"")
    response = client.post(
        "/api/datasets/upload",
        files={"file": ("empty.csv", file_bytes, "text/csv")}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"]

def test_list_and_get_dataset():
    csv_data = "order_date,sales\n2026-01-01,500\n"
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("sample.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    list_res = client.get("/api/datasets")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    get_res = client.get(f"/api/datasets/{ds_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == ds_id
