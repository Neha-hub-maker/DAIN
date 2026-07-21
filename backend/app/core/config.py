import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve workspace root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "DAIN MVP Platform"
    API_V1_STR: str = "/api"
    
    # SQLite Database configuration
    # By default, use sqlite+aiosqlite to allow async database queries.
    # The database file is located in the workspace root.
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/dain_mvp.db"
    
    # Credentials loaded from env
    GOOGLE_API_KEY: str = ""
    HF_TOKEN: str = ""
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
