from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger
from app.models import Base, engine  # Imports DatasetModel registration
from app.api.routes import health, datasets, investigations, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifespan events."""
    logger.info(f"Starting {settings.PROJECT_NAME} in [{settings.ENV}] mode...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")

    # Auto-seed initial benchmark dataset if DB is empty
    from app.database.database import SessionLocal
    from app.services.dataset_service import DatasetService
    import os

    db = SessionLocal()
    try:
        service = DatasetService(db)
        if not service.list_datasets() and os.path.exists("data/sample_sales.csv"):
            logger.info("Seeding initial benchmark dataset 'data/sample_sales.csv'...")
            service.ingest_existing_file("data/sample_sales.csv")
    except Exception as e:
        logger.warning(f"Could not seed initial dataset: {e}")
    finally:
        db.close()

    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Business Anomaly Detection & Root-Cause Analysis API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(health.router, prefix="/api")
app.include_router(datasets.router, prefix="/api")
app.include_router(investigations.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "title": settings.PROJECT_NAME,
        "status": "operational",
        "docs_url": "/docs"
    }
