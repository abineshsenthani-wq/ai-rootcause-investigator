from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DatasetMetaResponse(BaseModel):
    id: str
    filename: str
    upload_timestamp: datetime
    file_size_bytes: int
    row_count: int
    column_count: int
    primary_metric: Optional[str] = None
    date_column: Optional[str] = None
    date_min: Optional[str] = None
    date_max: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
