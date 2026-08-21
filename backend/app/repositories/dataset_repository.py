from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.dataset import DatasetModel
from app.models.chat import ChatMessageModel

class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dataset: DatasetModel) -> DatasetModel:
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    def get_by_id(self, dataset_id: str) -> Optional[DatasetModel]:
        return self.db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()

    def get_all(self) -> List[DatasetModel]:
        return self.db.query(DatasetModel).order_by(DatasetModel.upload_timestamp.desc()).all()

    def save_chat_message(self, message: ChatMessageModel) -> ChatMessageModel:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_chat_history(self, dataset_id: str) -> List[ChatMessageModel]:
        return (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.dataset_id == dataset_id)
            .order_by(ChatMessageModel.timestamp.asc())
            .all()
        )

    def delete_chat_history(self, dataset_id: str) -> int:
        deleted_count = (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.dataset_id == dataset_id)
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return deleted_count

