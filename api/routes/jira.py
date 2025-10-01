from fastapi import APIRouter, Depends
from services.jira_service import JiraService
from schemas.jira import JiraFieldsResponse, JiraUpdateRequest, JiraCommentRequest
from api.dependencies import get_jira_service

router = APIRouter(prefix="/jira-fields", tags=["Jira"])


@router.get("/{issue_key}", response_model=JiraFieldsResponse)
async def get_jira_fields(
    issue_key: str, jira_service: JiraService = Depends(get_jira_service)
):
    """Fetch specific fields for a Jira issue"""
    return jira_service.get_issue_fields(issue_key)


@router.put("/{issue_key}")
async def update_jira_fields(
    issue_key: str,
    request: JiraUpdateRequest,
    jira_service: JiraService = Depends(get_jira_service),
):
    """Update specific fields for a Jira issue"""
    return jira_service.update_issue_fields(issue_key, request.fields)


@router.post("/{issue_key}/comments")
async def create_jira_comment(
    issue_key: str,
    request: JiraCommentRequest,
    jira_service: JiraService = Depends(get_jira_service),
):
    """Create a comment on a Jira issue"""
    return jira_service.create_issue_comment(issue_key, {"body": request.body})
