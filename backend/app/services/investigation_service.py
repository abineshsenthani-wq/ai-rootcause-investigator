from sqlalchemy.orm import Session
from app.services.dataset_service import DatasetService

class InvestigationService:
    def __init__(self, db: Session):
        self.dataset_service = DatasetService(db)

    async def run_investigation(
        self,
        dataset_id: str,
        metric: str = None,
        start_period: str = None,
        end_period: str = None,
        question: str = None
    ) -> dict:
        return await self.dataset_service.run_investigation(
            dataset_id=dataset_id,
            metric=metric,
            start_period=start_period,
            end_period=end_period,
            question=question
        )
