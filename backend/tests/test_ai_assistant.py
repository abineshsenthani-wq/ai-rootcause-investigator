import pytest
import io
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine
from app.ai.router import QuestionRouter

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_question_router():
    assert QuestionRouter.route_question("Why did revenue decline?") == "ROOT_CAUSE"
    assert QuestionRouter.route_question("What are the top anomalies?") == "ANOMALY"
    assert QuestionRouter.route_question("Show revenue trend over time") == "TREND"
    assert QuestionRouter.route_question("Which region performed worst?") == "SEGMENT_ANALYSIS"

def test_chat_api_endpoint():
    csv_data = "order_date,revenue,region\n2026-06-01,100,West\n2026-07-01,50,West\n"
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("chat_test.csv", file_bytes, "text/csv")}
    )
    ds_id = upload_res.json()["id"]

    chat_res = client.post(
        f"/api/datasets/{ds_id}/chat",
        json={"question": "Why did revenue drop in July?"}
    )
    assert chat_res.status_code == 200
    data = chat_res.json()
    assert data["intent"] == "ROOT_CAUSE"
    assert "revenue" in data["ai_explanation"].lower() or "july" in data["ai_explanation"].lower()

    # Test GET history
    history_res = client.get(f"/api/datasets/{ds_id}/chat/history")
    assert history_res.status_code == 200
    messages = history_res.json()["messages"]
    assert len(messages) == 2 # 1 user + 1 assistant
    assert messages[0]["sender"] == "user"
    assert messages[0]["text"] == "Why did revenue drop in July?"
    assert messages[1]["sender"] == "assistant"

    # Test DELETE history
    del_res = client.delete(f"/api/datasets/{ds_id}/chat/history")
    assert del_res.status_code == 200
    assert del_res.json()["deleted_count"] == 2

    # Verify history is cleared
    empty_history_res = client.get(f"/api/datasets/{ds_id}/chat/history")
    assert empty_history_res.status_code == 200
    assert len(empty_history_res.json()["messages"]) == 0

