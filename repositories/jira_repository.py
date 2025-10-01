import requests
from core.config import Settings
from core.exceptions import BadRequest, NotFound, InternalServerError


class JiraRepository:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = settings.jira_base_url
        self.api_token = settings.atlassian_api_token

    def _create_headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def _build_issue_url(self, issue_key: str, api_version: str = "agile/1.0"):
        return f"https://{self.base_url}/rest/{api_version}/issue/{issue_key}"

    def get_issue(self, issue_key: str) -> dict:
        url = self._build_issue_url(issue_key)
        response = requests.get(url, headers=self._create_headers(), timeout=10)
        return self._handle_response(response)

    def update_issue(self, issue_key: str, data: dict) -> dict:
        url = self._build_issue_url(issue_key, "api/2")
        response = requests.put(url, headers=self._create_headers(), json=data)
        return self._handle_response(response)

    def create_comment(self, issue_key: str, data: dict) -> dict:
        url = f"{self._build_issue_url(issue_key, 'api/2')}/comment"
        response = requests.post(url, headers=self._create_headers(), json=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in (200, 201):
            return response.json()
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get("errorMessages", ["Bad Request"])[0]
            raise BadRequest(error_msg)
        elif response.status_code == 404:
            error_data = response.json()
            error_msg = error_data.get("errorMessages", ["Not Found"])[0]
            raise NotFound(error_msg)
        elif response.status_code == 500:
            raise InternalServerError(response.json())
        else:
            raise InternalServerError("Internal Server Error")
