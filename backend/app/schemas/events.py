from pydantic import BaseModel
from typing import Optional

class EventResponse(BaseModel):
    id: Optional[str] = None
    metric: str
    event_type: str
    start_period: str
    end_period: str
    previous_value: float
    current_value: float
    absolute_change: float
    percentage_change: float
    severity: str
