from repositories.jira_repository import JiraRepository
from schemas.jira import JiraFieldsResponse


class JiraService:
    def __init__(self, jira_repo: JiraRepository):
        self.jira_repo = jira_repo

    def get_issue_fields(self, issue_key: str) -> JiraFieldsResponse:
        """Get specific fields from a Jira issue"""
        result = self.jira_repo.get_issue(issue_key)

        fields = result.get("fields", {})
        epic = fields.get("epic", {})

        return JiraFieldsResponse(
            summary=fields.get("summary"),
            description=fields.get("description"),
            story_points=fields.get("customfield_10018"),
            acceptance_criteria=fields.get("customfield_11518"),
            epic_link=epic.get("self") if epic else None,
        )

    def update_issue_fields(self, issue_key: str, data: dict) -> dict:
        """Update Jira issue fields"""
        self.jira_repo.update_issue(issue_key, data)
        return {"message": "Successfully updated issue!"}

    def create_issue_comment(self, issue_key: str, data: dict) -> dict:
        """Create a comment on a Jira issue"""
        return self.jira_repo.create_comment(issue_key, data)
