# app/core/config.py
"""
Application Configuration with Environment Variables
"""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variables support"""

    # API
    API_HOST: str = Field(default="127.0.0.1", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    # Auth
    SECRET_KEY: str = Field(default="your-secret-key-change-this-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # RAG
    RAG_URL: str = Field(default="http://localhost:8001", env="RAG_URL")
    HF_HUB_ENABLE_HF_TRANSFER: int = Field(default=0, env="HF_HUB_ENABLE_HF_TRANSFER")
    HF_HUB_DOWNLOAD_TIMEOUT: int = Field(default=300, env="HF_HUB_DOWNLOAD_TIMEOUT")

    # Models
    MODELS_DIR: str = Field(default="./models", env="MODELS_DIR")
    DATA_DIR: str = Field(default="./data", env="DATA_DIR")

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"], env="BACKEND_CORS_ORIGINS"
    )

    PROJECT_NAME: str = Field(default="Customer Support AI", env="PROJECT_NAME")
    VERSION: str = Field(default="1.0.0", env="VERSION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


# Create global settings instance
settings = Settings()
