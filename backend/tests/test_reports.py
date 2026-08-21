import pytest
import io
from fastapi.testclient import TestClient
from app.main import app
from app.models.database import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_pdf_report_download():
    csv_data = "order_date,revenue,region\n2026-06-01,100,West\n2026-07-01,50,West\n"
    file_bytes = io.BytesIO(csv_data.encode("utf-8"))
    upload_res = client.post(
        "/api/datasets/upload",
        files={"file": ("report_test.csv", file_bytes, "text/csv")}
    )
    ds_id = upload_res.json()["id"]

    report_res = client.get(f"/api/datasets/{ds_id}/report")
    assert report_res.status_code == 200
    assert report_res.headers["content-type"] == "application/pdf"
    assert len(report_res.content) > 500  # Non-empty PDF payload
    assert report_res.content.startswith(b"%PDF") # Valid PDF magic header
