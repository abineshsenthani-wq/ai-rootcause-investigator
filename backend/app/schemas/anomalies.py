from pydantic import BaseModel
from typing import List, Dict, Any, Union

class AnomalyItem(BaseModel):
    row_id: int
    metric: str
    value: float
    expected_range: str
    anomaly_score: float
    method: str
    severity: str

class AnomalyResponse(BaseModel):
    metric: str
    total_anomalies: int
    summary_by_method: Dict[str, int]
    anomalies: List[AnomalyItem]
