from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime

class FactorScoreBreakdown(BaseModel):
    contribution_score: float
    correlation_score: float
    temporal_alignment_score: float
    anomaly_strength_score: float
    data_coverage_score: float

class PotentialFactorItem(BaseModel):
    factor_name: str
    dimension: str
    segment: str
    metric_change_pct: float
    contribution_pct: float
    evidence_score: float
    score_breakdown: FactorScoreBreakdown
    evidence_label: str

class HypothesisItem(BaseModel):
    factor: str
    evidence_score: float
    evidence_label: str
    statement: str

class InvestigationRequest(BaseModel):
    metric: Optional[str] = None
    start_period: Optional[str] = None
    end_period: Optional[str] = None
    question: Optional[str] = None

class InvestigationResponse(BaseModel):
    event: Dict[str, Any]
    summary: str
    facts: List[str]
    potential_factors: List[PotentialFactorItem]
    evidence: List[Dict[str, Any]]
    causal_inference: Optional[List[Dict[str, Any]]] = None
    forecast: Optional[Dict[str, Any]] = None
    similar_incidents: Optional[List[Dict[str, Any]]] = None
    anomalies: List[Dict[str, Any]]
    hypotheses: List[HypothesisItem]
    recommendations: List[str]
    confidence: float
    limitations: List[str]
    ai_explanation: Optional[str] = None

class SimulationRequest(BaseModel):
    target_metric: str
    driver_adjustments: Dict[str, float]

class SimulationResponse(BaseModel):
    target_metric: str
    baseline_mean: float
    simulated_mean: float
    total_predicted_change: float
    total_percentage_impact: float
    variable_impacts: List[Dict[str, Any]]
    scenario_summary: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    intent: str
    question: str
    evidence: Dict[str, Any]
    ai_explanation: str

class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    dataset_id: str
    sender: str
    text: str
    intent: Optional[str] = None
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    dataset_id: str
    messages: List[ChatMessageResponse]
