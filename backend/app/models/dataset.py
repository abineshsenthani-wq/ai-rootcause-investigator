from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime, timezone
import uuid
from app.models.database import Base

class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    upload_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    file_size_bytes = Column(Integer, nullable=False)
    row_count = Column(Integer, nullable=False, default=0)
    column_count = Column(Integer, nullable=False, default=0)
    
    # Detected metadata
    primary_metric = Column(String(100), nullable=True)
    date_column = Column(String(100), nullable=True)
    date_min = Column(String(50), nullable=True)
    date_max = Column(String(50), nullable=True)
