from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone
import uuid
from app.models.database import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    metric = Column(String(100), nullable=False)
    event_type = Column(String(50), nullable=False) # DROP or SPIKE
    start_period = Column(String(50), nullable=False)
    end_period = Column(String(50), nullable=False)
    previous_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    absolute_change = Column(Float, nullable=False)
    percentage_change = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
