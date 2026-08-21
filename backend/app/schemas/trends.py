from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TrendPoint(BaseModel):
    order_date: Optional[str] = None
    revenue: Optional[float] = None
    previous_value: Optional[float] = None
    absolute_change: Optional[float] = None
    percentage_change: Optional[float] = None
    rolling_avg_3: Optional[float] = None

class TrendResponse(BaseModel):
    metric: str
    date_column: str
    granularity: str
    trend_points: List[Dict[str, Any]]
    summary: Dict[str, Any]
