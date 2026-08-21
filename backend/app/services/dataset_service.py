import os
import uuid
import pandas as pd
import numpy as np
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logging import logger
from app.models.dataset import DatasetModel
from app.models.chat import ChatMessageModel
from app.repositories.dataset_repository import DatasetRepository
from app.analysis.profiling import DataProfiler
from app.analysis.trends import TimeTrendEngine
from app.analysis.events import EventDetectionEngine
from app.analysis.anomalies import AnomalyAnalysisEngine
from app.analysis.investigation import InvestigationEngine
from app.ai.llm_provider import LLMProvider
from app.ai.router import QuestionRouter
from app.services.report_service import ReportService

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

class DatasetService:
    def __init__(self, db: Session):
        self.repository = DatasetRepository(db)

    @staticmethod
    def _ensure_date_column(df: pd.DataFrame, existing_date_col: str = None) -> (pd.DataFrame, str):
        """Ensures a valid date column exists. If missing, creates a synthetic daily timestamp column."""
        if existing_date_col and existing_date_col in df.columns:
            return df, existing_date_col

        # Try auto-detecting date columns
        date_keywords = ["date", "time", "timestamp", "year", "month", "day", "dt", "period", "created_at"]
        for col in df.columns:
            if any(kw in col.lower() for kw in date_keywords):
                converted = pd.to_datetime(df[col], errors="coerce", format="mixed").dropna()
                if len(converted) > 0:
                    return df, col

        # Try converting any string/object column to datetime
        for col in df.columns:
            if df[col].dtype == object or pd.api.types.is_string_dtype(df[col]):
                converted = pd.to_datetime(df[col], errors="coerce", format="mixed").dropna()
                if len(converted) / max(len(df), 1) > 0.7:
                    return df, col

        # Synthetic fallback: create 'synthetic_date' starting from 2026-01-01
        df = df.copy()
        df["synthetic_date"] = pd.date_range(start="2026-01-01", periods=len(df), freq="D").strftime("%Y-%m-%d")
        return df, "synthetic_date"

    @staticmethod
    def _resolve_target_metric(df: pd.DataFrame, requested_metric: str = None, default_metric: str = None) -> str:
        """Resolves target metric. Filters out identifier columns and falls back to actual numerical business metrics."""
        id_keywords = {"id", "order_id", "customer_id", "row_id", "uuid", "transaction_id", "sku"}

        def is_valid_metric(col: str) -> bool:
            if not col or col not in df.columns:
                return False
            col_lower = col.lower()
            if col_lower.endswith("_id") or col_lower in id_keywords:
                return False
            return pd.api.types.is_numeric_dtype(df[col])

        if requested_metric and is_valid_metric(requested_metric):
            return requested_metric
        if default_metric and is_valid_metric(default_metric):
            return default_metric
        if requested_metric and requested_metric in df.columns:
            return requested_metric

        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        valid_metrics = [c for c in num_cols if not c.lower().endswith("_id") and c.lower() not in id_keywords]

        # Prioritize key business metrics if present
        metric_keywords = ["revenue", "sales", "profit", "amount", "total", "quantity", "price", "spend", "cost"]
        for kw in metric_keywords:
            for col in valid_metrics:
                if kw in col.lower():
                    return col

        if valid_metrics:
            return valid_metrics[0]
        if num_cols:
            return num_cols[0]

        df["metric_val"] = 1.0
        return "metric_val"

    async def save_and_profile_upload(self, file: UploadFile) -> DatasetModel:
        filename = file.filename or "uploaded_dataset.csv"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        content = await file.read()
        file_size = len(content)

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty (0 bytes)."
            )

        dataset_id = str(uuid.uuid4())
        safe_filename = f"{dataset_id}{ext}"
        file_path = os.path.join(settings.DATA_STORAGE_DIR, safe_filename)

        with open(file_path, "wb") as f:
            f.write(content)

        try:
            df = pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Malformed dataset file. Could not parse as {ext.upper()}: {str(e)}"
            )

        if df.empty:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded dataset contains no data rows."
            )

        row_count, column_count = df.shape

        # Auto-detect date column and date boundaries
        df, date_col = self._ensure_date_column(df)
        converted_date = pd.to_datetime(df[date_col], errors="coerce", format="mixed").dropna()
        date_min = str(converted_date.min().date()) if len(converted_date) > 0 else "2026-01-01"
        date_max = str(converted_date.max().date()) if len(converted_date) > 0 else "2026-07-31"

        # Auto-detect primary metric
        metric_col = self._resolve_target_metric(df)

        dataset = DatasetModel(
            id=dataset_id,
            filename=filename,
            file_path=file_path,
            file_size_bytes=file_size,
            row_count=row_count,
            column_count=column_count,
            primary_metric=metric_col,
            date_column=date_col,
            date_min=date_min,
            date_max=date_max
        )

        return self.repository.create(dataset)

    def ingest_existing_file(self, source_path: str, display_filename: str = None) -> DatasetModel:
        if not os.path.exists(source_path):
            return None
        filename = display_filename or os.path.basename(source_path)
        ext = os.path.splitext(filename)[1].lower()
        file_size = os.path.getsize(source_path)

        dataset_id = str(uuid.uuid4())
        safe_filename = f"{dataset_id}{ext}"
        dest_path = os.path.join(settings.DATA_STORAGE_DIR, safe_filename)
        os.makedirs(settings.DATA_STORAGE_DIR, exist_ok=True)
        import shutil
        shutil.copy(source_path, dest_path)

        df = pd.read_csv(dest_path) if ext == ".csv" else pd.read_excel(dest_path)
        row_count, column_count = df.shape
        df, date_col = self._ensure_date_column(df)
        converted_date = pd.to_datetime(df[date_col], errors="coerce", format="mixed").dropna()
        date_min = str(converted_date.min().date()) if len(converted_date) > 0 else "2026-01-01"
        date_max = str(converted_date.max().date()) if len(converted_date) > 0 else "2026-07-31"
        metric_col = self._resolve_target_metric(df)

        dataset = DatasetModel(
            id=dataset_id,
            filename=filename,
            file_path=dest_path,
            file_size_bytes=file_size,
            row_count=row_count,
            column_count=column_count,
            primary_metric=metric_col,
            date_column=date_col,
            date_min=date_min,
            date_max=date_max
        )
        return self.repository.create(dataset)


    def get_dataset(self, dataset_id: str) -> DatasetModel:
        dataset = self.repository.get_by_id(dataset_id)
        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset with ID '{dataset_id}' not found."
            )
        return dataset

    def list_datasets(self) -> list[DatasetModel]:
        return self.repository.get_all()

    def _read_df(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset file missing on disk."
            )
        ext = os.path.splitext(file_path)[1].lower()
        return pd.read_csv(file_path) if ext == ".csv" else pd.read_excel(file_path)

    def profile_dataset(self, dataset_id: str) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        profile_results = DataProfiler.profile_dataset(df)
        return {
            "dataset_id": dataset.id,
            "filename": dataset.filename,
            **profile_results
        }

    def get_trends(self, dataset_id: str, metric: str = None, granularity: str = None) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        df, date_col = self._ensure_date_column(df, dataset.date_column)
        target_metric = self._resolve_target_metric(df, metric, dataset.primary_metric)

        return TimeTrendEngine.calculate_trend(
            df=df,
            date_col=date_col,
            metric_col=target_metric,
            granularity=granularity
        )

    def detect_events(self, dataset_id: str, metric: str = None, granularity: str = None) -> list:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        df, date_col = self._ensure_date_column(df, dataset.date_column)
        target_metric = self._resolve_target_metric(df, metric, dataset.primary_metric)

        return EventDetectionEngine.detect_events(
            df=df,
            date_col=date_col,
            metric_col=target_metric,
            granularity=granularity
        )

    def detect_anomalies(self, dataset_id: str, metric: str = None) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        target_metric = self._resolve_target_metric(df, metric, dataset.primary_metric)
        return AnomalyAnalysisEngine.run_anomaly_detection(df, metric=target_metric)

    async def run_investigation(
        self,
        dataset_id: str,
        metric: str = None,
        start_period: str = None,
        end_period: str = None,
        question: str = None
    ) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        df, date_col = self._ensure_date_column(df, dataset.date_column)
        target_metric = self._resolve_target_metric(df, metric, dataset.primary_metric)

        result = InvestigationEngine.investigate(
            df=df,
            target_metric=target_metric,
            start_period=start_period,
            end_period=end_period,
            user_question=question
        )

        ai_explanation = await LLMProvider.generate_explanation(result)
        result["ai_explanation"] = ai_explanation
        return result

    async def chat_with_dataset(self, dataset_id: str, question: str) -> dict:
        intent = QuestionRouter.route_question(question)
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)

        df, date_col = self._ensure_date_column(df, dataset.date_column)
        target_metric = self._resolve_target_metric(df, None, dataset.primary_metric)

        investigation_result = InvestigationEngine.investigate(
            df=df,
            target_metric=target_metric,
            user_question=question
        )

        ai_explanation = await LLMProvider.generate_explanation(investigation_result)

        # Persist User Question
        user_msg = ChatMessageModel(
            dataset_id=dataset_id,
            sender="user",
            text=question,
            intent=intent
        )
        self.repository.save_chat_message(user_msg)

        # Persist Assistant Response
        assistant_msg = ChatMessageModel(
            dataset_id=dataset_id,
            sender="assistant",
            text=ai_explanation,
            intent=intent
        )
        self.repository.save_chat_message(assistant_msg)

        return {
            "intent": intent,
            "question": question,
            "evidence": investigation_result,
            "ai_explanation": ai_explanation
        }

    def get_chat_history(self, dataset_id: str) -> dict:
        dataset = self.get_dataset(dataset_id)
        messages = self.repository.get_chat_history(dataset.id)
        return {
            "dataset_id": dataset.id,
            "messages": messages
        }

    def clear_chat_history(self, dataset_id: str) -> dict:
        dataset = self.get_dataset(dataset_id)
        deleted_count = self.repository.delete_chat_history(dataset.id)
        return {
            "dataset_id": dataset.id,
            "deleted_count": deleted_count,
            "message": f"Successfully deleted {deleted_count} message(s) from chat history."
        }

    async def generate_pdf_report(self, dataset_id: str) -> bytes:
        investigation = await self.run_investigation(dataset_id)
        return ReportService.generate_pdf_report(investigation)

    def simulate_scenario(self, dataset_id: str, target_metric: str, driver_adjustments: dict) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)
        from app.analysis.simulator import WhatIfSimulator
        metric = self._resolve_target_metric(df, target_metric, dataset.primary_metric)
        return WhatIfSimulator.simulate_counterfactual(df, metric, driver_adjustments)

    def get_forecast(self, dataset_id: str, metric: str = None, periods: int = 12) -> dict:
        dataset = self.get_dataset(dataset_id)
        df = self._read_df(dataset.file_path)
        from app.analysis.forecasting import ForecastingEngine
        df, date_col = self._ensure_date_column(df, dataset.date_column)
        target_metric = self._resolve_target_metric(df, metric, dataset.primary_metric)
        return ForecastingEngine.forecast_metric(df, date_col, target_metric, periods_ahead=periods)


