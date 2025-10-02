from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):

    environment: str = "development"

    # Jira
    atlassian_api_token: str
    jira_base_url: str

    # Database - single connection string
    database_url: str

    # Redis - single connection string
    redis_url: str

    # AWS Service
    sqs_queue_url: str

    # App
    app_name: str = "IA QA AGENT"

    # OpenAI
    open_ai_api_key: Optional[str] = None

    class Config:
        env_file = None if os.getenv("ENVIRONMENT") == "production" else ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Development: Reads from .env file
    Production: Reads from system environment variables
    """
    return Settings()
