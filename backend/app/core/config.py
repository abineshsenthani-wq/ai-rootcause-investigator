from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Root-Cause Investigator"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"]
    
    DATABASE_URL: str = "sqlite:///./investigator.db"
    DATA_STORAGE_DIR: str = "./data/uploads"
    
    LLM_PROVIDER: str = "fallback"  # options: "openai", "anthropic", "fallback"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Ensure data storage directory exists
os.makedirs(settings.DATA_STORAGE_DIR, exist_ok=True)
