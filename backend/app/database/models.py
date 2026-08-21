from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey
from datetime import datetime, timezone
import uuid
from app.database.database import Base

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

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    metric = Column(String(100), nullable=False)
    event_type = Column(String(50), nullable=False)
    start_period = Column(String(50), nullable=False)
    end_period = Column(String(50), nullable=False)
    previous_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    absolute_change = Column(Float, nullable=False)
    percentage_change = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    sender = Column(String(20), nullable=False)
    text = Column(Text, nullable=False)
    intent = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class InvestigationModel(Base):
    __tablename__ = "investigations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    metric = Column(String(100), nullable=False)
    start_period = Column(String(50), nullable=True)
    end_period = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=False, default=0.0)
    ai_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class FindingModel(Base):
    __tablename__ = "findings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), ForeignKey("investigations.id"), nullable=False)
    finding_type = Column(String(20), nullable=False) # 'FACT', 'HYPOTHESIS', 'RECOMMENDATION'
    statement = Column(Text, nullable=False)
    evidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
