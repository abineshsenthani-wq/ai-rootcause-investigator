from pydantic import BaseModel
from typing import Dict, Any, List

class ColumnClassification(BaseModel):
    numerical_columns: List[str]
    categorical_columns: List[str]
    date_columns: List[str]
    boolean_columns: List[str]
    identifier_columns: List[str]

class DataQualitySummary(BaseModel):
    total_rows: int
    total_columns: int
    missing_cells: int
    missing_percentage: float
    duplicate_rows: int
    constant_columns: List[str]
    empty_columns: List[str]
    is_clean: bool

class ProfileResponse(BaseModel):
    dataset_id: str
    filename: str
    classification: ColumnClassification
    quality: DataQualitySummary
    column_stats: Dict[str, Any]
