from fastapi import APIRouter, Depends, UploadFile, File, Query, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.schemas.dataset import DatasetMetaResponse
from app.schemas.profiling import ProfileResponse
from app.schemas.trends import TrendResponse
from app.schemas.events import EventResponse
from app.schemas.anomalies import AnomalyResponse
from app.schemas.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse
)
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/upload", response_model=DatasetMetaResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads and validates a CSV/Excel business dataset."""
    service = DatasetService(db)
    return await service.save_and_profile_upload(file)

@router.get("", response_model=List[DatasetMetaResponse])
def list_datasets(db: Session = Depends(get_db)):
    """Lists all uploaded datasets."""
    service = DatasetService(db)
    return service.list_datasets()

@router.get("/{dataset_id}", response_model=DatasetMetaResponse)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    """Retrieves dataset metadata by ID."""
    service = DatasetService(db)
    return service.get_dataset(dataset_id)

@router.get("/{dataset_id}/profile", response_model=ProfileResponse)
def get_dataset_profile(dataset_id: str, db: Session = Depends(get_db)):
    """Generates automated column statistical profile and data quality assessment."""
    service = DatasetService(db)
    return service.profile_dataset(dataset_id)

@router.get("/{dataset_id}/trends", response_model=TrendResponse)
def get_dataset_trends(
    dataset_id: str,
    metric: Optional[str] = Query(None, description="Target numerical metric to analyze"),
    granularity: Optional[str] = Query(None, description="Aggregation granularity: D, W, M, Q, Y"),
    db: Session = Depends(get_db)
):
    """Calculates metric time trend, rolling average, and period-over-period percentage shifts."""
    service = DatasetService(db)
    return service.get_trends(dataset_id, metric=metric, granularity=granularity)

@router.get("/{dataset_id}/events", response_model=List[EventResponse])
def get_dataset_events(
    dataset_id: str,
    metric: Optional[str] = Query(None, description="Target numerical metric"),
    granularity: Optional[str] = Query(None, description="Aggregation granularity"),
    db: Session = Depends(get_db)
):
    """Scans metrics for unusual business events (drops/spikes) and severity classification."""
    service = DatasetService(db)
    return service.detect_events(dataset_id, metric=metric, granularity=granularity)

@router.get("/{dataset_id}/anomalies", response_model=AnomalyResponse)
def get_dataset_anomalies(
    dataset_id: str,
    metric: Optional[str] = Query(None, description="Target numerical metric"),
    db: Session = Depends(get_db)
):
    """Runs multi-method anomaly detection (IQR, Z-Score, Isolation Forest)."""
    service = DatasetService(db)
    return service.detect_anomalies(dataset_id, metric=metric)

@router.post("/{dataset_id}/investigate", response_model=InvestigationResponse)
async def run_dataset_investigation(
    dataset_id: str,
    req: InvestigationRequest,
    db: Session = Depends(get_db)
):
    """Performs full root-cause investigation and generates evidence-grounded AI explanation."""
    service = DatasetService(db)
    return await service.run_investigation(
        dataset_id=dataset_id,
        metric=req.metric,
        start_period=req.start_period,
        end_period=req.end_period,
        question=req.question
    )

@router.post("/{dataset_id}/chat", response_model=ChatResponse)
async def chat_with_dataset(
    dataset_id: str,
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    """Routes user question to statistical engine and generates evidence-backed natural language response."""
    service = DatasetService(db)
    return await service.chat_with_dataset(dataset_id, req.question)

@router.get("/{dataset_id}/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """Retrieves stored chat conversation history for the dataset."""
    service = DatasetService(db)
    return service.get_chat_history(dataset_id)

@router.delete("/{dataset_id}/chat/history")
def clear_chat_history(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """Clears stored chat conversation history for the dataset."""
    service = DatasetService(db)
    return service.clear_chat_history(dataset_id)


@router.get("/{dataset_id}/report")
async def download_investigation_report(
    dataset_id: str,
    db: Session = Depends(get_db)
):
    """Generates and downloads a printable PDF investigation report."""
    service = DatasetService(db)
    pdf_bytes = await service.generate_pdf_report(dataset_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=investigation_report_{dataset_id}.pdf"}
    )
