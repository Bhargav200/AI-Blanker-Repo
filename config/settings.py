import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI PII Redactor"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./database/pii_redactor.db"
    
    # Storage
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    INPUT_DIR: Path = BASE_DIR / "storage" / "input"
    OUTPUT_DIR: Path = BASE_DIR / "storage" / "output"
    LOGS_DIR: Path = BASE_DIR / "storage" / "logs"
    TEMP_DIR: Path = BASE_DIR / "storage" / "temp"
    
    # OCR
    TESSERACT_CMD: Optional[str] = None # Path to tesseract executable
    
    # NLP
    SPACY_MODEL: str = "en_core_web_sm"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Ensure directories exist
def ensure_dirs():
    settings = Settings()
    for dir_path in [settings.INPUT_DIR, settings.OUTPUT_DIR, settings.LOGS_DIR, settings.TEMP_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    (settings.BASE_DIR / "database").mkdir(parents=True, exist_ok=True)

settings = Settings()
ensure_dirs()
