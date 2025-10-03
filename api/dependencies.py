from fastapi import Depends
from core.config import get_settings, Settings
from repositories.jira_repository import JiraRepository
from services.jira_service import JiraService
from repositories.health_repository import HealthRepository
from services.health_service import HealthService
from sqlalchemy.orm import Session
from db.session import get_db
from repositories.message_repository import MessageRepository


def get_jira_repository(settings: Settings = Depends(get_settings)) -> JiraRepository:
    return JiraRepository(settings)


def get_jira_service(
    jira_repo: JiraRepository = Depends(get_jira_repository),
) -> JiraService:
    return JiraService(jira_repo)


def get_health_repository(
    settings: Settings = Depends(get_settings),
) -> HealthRepository:
    return HealthRepository(settings)


def get_health_service(
    health_repo: HealthRepository = Depends(get_health_repository),
    settings: Settings = Depends(get_settings),
) -> HealthService:
    return HealthService(health_repo, settings)


def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    return MessageRepository(db)
