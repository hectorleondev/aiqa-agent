from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Jira
    atlassian_api_token: str = os.getenv("ATLASSIAN_API_TOKEN")
    jira_base_url: str = os.getenv("JIRA_BASE_URL")

    # Database
    database_url: str = os.getenv("DATABASE_URL")

    # Redis
    redis_url: str = os.getenv("REDIS_URL")

    # AWS
    sqs_queue_url: str = os.environ.get("SQS_QUEUE_URL")

    # App
    app_name: str = "IA QA AGENT"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
