from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from app.models.database import get_db
from app.schemas.health import HealthResponse
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
def check_health(db: Session = Depends(get_db)):
    """Verifies backend system operational status, DB connection, and storage accessibility."""
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    storage_writable = os.access(settings.DATA_STORAGE_DIR, os.W_OK)

    return HealthResponse(
        status="healthy" if (db_ok and storage_writable) else "degraded",
        version="1.0.0",
        environment=settings.ENV,
        database_connected=db_ok,
        storage_directory_writable=storage_writable,
        details={
            "llm_provider": settings.LLM_PROVIDER,
            "data_storage_dir": settings.DATA_STORAGE_DIR
        }
    )
