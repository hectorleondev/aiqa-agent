from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
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
    open_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env


@lru_cache()
def get_settings() -> Settings:
    return Settings()