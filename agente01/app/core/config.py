"""Application configuration — all secrets read from environment variables."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Agente01 - Relatório Técnico Automatizado"
    APP_ENV: str = "DEV"  # DEV | PROD
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://agente01:agente01pass@postgres:5432/agente01"
    DATABASE_URL_SYNC: str = "postgresql://agente01:agente01pass@postgres:5432/agente01"

    # JWT
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 24h

    # Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # MinIO / S3
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "agente01-evidencias"
    MINIO_USE_SSL: bool = False

    # LLM
    LLM_PROVIDER: str = "openai"  # openai | claude | local
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    CLAUDE_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    LOCAL_LLM_URL: Optional[str] = None

    # Digital Signature
    SIGNING_PRIVATE_KEY_PATH: Optional[str] = None
    SIGNING_PRIVATE_KEY_PEM: Optional[str] = None

    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = 100
    ALLOWED_IMAGE_EXTENSIONS: str = ".jpg,.jpeg,.png,.bmp,.tiff,.gif"
    ALLOWED_VIDEO_EXTENSIONS: str = ".mp4,.avi,.mov,.mkv,.wmv"

    # LGPD
    DATA_RETENTION_DAYS: int = 365 * 5  # 5 years default
    PURGE_REQUIRES_ADMIN: bool = True

    # LibreOffice
    LIBREOFFICE_PATH: str = "libreoffice"

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
