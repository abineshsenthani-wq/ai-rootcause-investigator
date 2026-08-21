from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
import uuid
from app.models.database import Base

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=False)
    sender = Column(String(20), nullable=False) # 'user' or 'assistant'
    text = Column(Text, nullable=False)
    intent = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
