from pydantic import BaseModel
from typing import Optional


class JiraFieldsResponse(BaseModel):
    summary: Optional[str]
    description: Optional[str]
    story_points: Optional[float]
    acceptance_criteria: Optional[str]
    epic_link: Optional[str]


class JiraUpdateRequest(BaseModel):
    fields: dict


class JiraCommentRequest(BaseModel):
    body: str
