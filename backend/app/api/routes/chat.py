from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.investigation import (
    ChatRequest,
    ChatResponse,
    ChatHistoryResponse
)
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["AI Chat"])

@router.post("/{dataset_id}/chat", response_model=ChatResponse)
async def chat_with_dataset(
    dataset_id: str,
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    """Routes user question to statistical engine and generates evidence-backed response."""
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
