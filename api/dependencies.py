from fastapi import Depends
from core.config import get_settings, Settings
from repositories.jira_repository import JiraRepository
from services.jira_service import JiraService


def get_jira_repository(settings: Settings = Depends(get_settings)) -> JiraRepository:
    return JiraRepository(settings)


def get_jira_service(
    jira_repo: JiraRepository = Depends(get_jira_repository),
) -> JiraService:
    return JiraService(jira_repo)
