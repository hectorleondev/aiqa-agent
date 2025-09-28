from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .decorators import pretty_resp
from .parser import (
    send_fields_for_jira_issue,
    update_fields_for_jira_issue,
    create_fields_for_jira_issue_comments,
check_status,
)

app = FastAPI()


@app.get("/health", response_model=None, status_code=200)
def root() -> dict[str, str]:
    """
    Health check endpoint

    Returns:
        dict: Status information including health status, message, and current
              time
    """

    return {
        "status": "healthy",
        "message": "IA QA AGENT is running smoothly",
        "time": datetime.now().isoformat(),
    }


@app.get("/jira-fields/{issue_key}")
@pretty_resp
def get_jira_fields(issue_key: str):
    """
    Fetches and returns specific fields for a Jira issue.

    Args:
        issue_key (str): The Jira issue key to look up.

    Returns:
        JSONResponse: A JSON object containing summary, description, story points,
                      acceptance criteria, and epic link for the given issue.
    """
    fields = send_fields_for_jira_issue(issue_key)
    return JSONResponse(content=fields, status_code=200)


@app.put("/jira-fields/{issue_key}")
@pretty_resp
def update_jira_fields(issue_key: str, data: dict):
    """
    Update specific fields for a Jira issue.

    Args:
        issue_key (str): The Jira issue key to look up.

    Returns:
        JSONResponse: message indicating success or failure of the update operation.
    """
    fields = update_fields_for_jira_issue(issue_key, data)
    return JSONResponse(content=fields, status_code=200)


@app.post("/jira-fields/{issue_key}/comments")
@pretty_resp
def update_jira_fields(issue_key: str, data: dict):
    """
    Update specific fields for a Jira issue.

    Args:
        issue_key (str): The Jira issue key to look up.

    Returns:
        JSONResponse: message indicating success or failure of the update operation.
    """
    fields = create_fields_for_jira_issue_comments(issue_key, data)
    return JSONResponse(content=fields, status_code=200)


@app.get("/cache-status")
@pretty_resp
def cache_status():
    fields = check_status()
    return JSONResponse(content=fields, status_code=200)