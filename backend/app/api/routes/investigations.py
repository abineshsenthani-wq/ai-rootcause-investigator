from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.investigation import InvestigationRequest, InvestigationResponse, SimulationRequest, SimulationResponse
from app.services.investigation_service import InvestigationService
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["Investigations"])

@router.post("/{dataset_id}/investigate", response_model=InvestigationResponse)
async def run_dataset_investigation(
    dataset_id: str,
    req: InvestigationRequest,
    db: Session = Depends(get_db)
):
    """Performs full root-cause investigation and generates evidence-grounded AI explanation."""
    service = InvestigationService(db)
    return await service.run_investigation(
        dataset_id=dataset_id,
        metric=req.metric,
        start_period=req.start_period,
        end_period=req.end_period,
        question=req.question
    )

@router.post("/{dataset_id}/simulate", response_model=SimulationResponse)
def simulate_counterfactual_scenario(
    dataset_id: str,
    req: SimulationRequest,
    db: Session = Depends(get_db)
):
    """Simulates What-If counterfactual shifts based on driver variable adjustments."""
    service = DatasetService(db)
    return service.simulate_scenario(
        dataset_id=dataset_id,
        target_metric=req.target_metric,
        driver_adjustments=req.driver_adjustments
    )

@router.get("/{dataset_id}/forecast")
def get_metric_forecast(
    dataset_id: str,
    metric: str = Query(None),
    periods: int = Query(12),
    db: Session = Depends(get_db)
):
    """Generates 30-day/12-period trend forecast with 95% confidence intervals."""
    service = DatasetService(db)
    return service.get_forecast(dataset_id=dataset_id, metric=metric, periods=periods)
