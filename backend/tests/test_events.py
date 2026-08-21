import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine
from app.analysis.events import EventDetectionEngine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_event_severity_scoring():
    assert EventDetectionEngine.calculate_severity(-35.0) == "CRITICAL"
    assert EventDetectionEngine.calculate_severity(-22.0) == "HIGH"
    assert EventDetectionEngine.calculate_severity(12.0) == "MEDIUM"
    assert EventDetectionEngine.calculate_severity(-6.0) == "LOW"
    assert EventDetectionEngine.calculate_severity(2.0) == "NORMAL"

def test_event_detection_api():
    csv_data = (
        "order_date,revenue\n"
        "2026-06-01,1000\n"
        "2026-06-20,1000\n"
        "2026-07-01,700\n"
        "2026-07-20,700\n"
    )
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("event_test.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 201
    ds_id = upload_res.json()["id"]

    event_res = client.get(f"/api/datasets/{ds_id}/events?granularity=M")
    assert event_res.status_code == 200
    events = event_res.json()

    assert len(events) == 1
    event = events[0]
    assert event["event_type"] == "METRIC_DROP"
    assert event["percentage_change"] == -30.0
    assert event["severity"] == "CRITICAL"
