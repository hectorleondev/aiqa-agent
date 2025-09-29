import os
import requests
import dotenv
from .exceptions import BadRequest, NotFound, InternalServerError
import psycopg2
import redis

dotenv.load_dotenv()

ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
database_url = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")


def create_jira_headers(api_token):
    """Create headers for Jira API requests."""
    return {"Accept": "application/json", "Authorization": f"Bearer {api_token}"}


def build_board_issue_url(base_url, issue_id):
    """Build the URL for a Jira issue."""
    return f"https://{base_url}/rest/agile/1.0/issue/{issue_id}"


def build_board_issue_url_v2(base_url, issue_id):
    """Build the URL for a Jira issue."""
    return f"https://{base_url}/rest/api/2/issue/{issue_id}"


def fetch_board_issues(url, headers):
    "" "Fetch issue data from Jira board." ""
    response = requests.get(url, headers=headers, timeout=10)
    return response


def put_board_issues(url, headers, data):
    """Put issue data from Jira board."""
    response = requests.put(url, headers=headers, json=data)
    return response


def post_board_issues_comments(url, headers, data):
    """POST issue comments from Jira board."""
    response = requests.post(url, headers=headers, json=data)
    return response


def extract_fields_from_response(response):
    """Extract fields from Jira API response."""
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    if response.status_code == 201:
        response_data = response.json()
        return response_data
    if response.status_code == 204:
        return {}
    elif response.status_code == 400:
        response_data = response.json()
        errorMessages = response_data.get("errorMessages")
        if isinstance(errorMessages, list) and errorMessages:
            raise BadRequest(errorMessages[0])
        raise BadRequest("Bad Request")
    elif response.status_code == 404:
        response_data = response.json()
        errorMessages = response_data.get("errorMessages")
        if isinstance(errorMessages, list) and errorMessages:
            raise NotFound(errorMessages[0])
        raise NotFound("NotFound")
    elif response.status_code == 500:
        response_data = response.json()
        raise InternalServerError(response_data)
    else:
        raise InternalServerError("Internal Server Error")


def send_fields_for_jira_issue(issue_key):
    """
    Fetch specific fields for a Jira issue and return as a dict.
    """
    headers = create_jira_headers(ATLASSIAN_API_TOKEN)
    issue_url = build_board_issue_url(JIRA_BASE_URL, issue_key)
    print(f"Fetching issues from board: {issue_url}")

    response = fetch_board_issues(issue_url, headers)
    result = extract_fields_from_response(response)

    fields = result.get("fields", {})
    summary = fields.get("summary")
    description = fields.get("description")
    story_points = fields.get("customfield_10018")
    acceptance_criteria = fields.get("customfield_11518")
    epic_link = fields.get("epic", {}).get("self") if fields.get("epic") else None

    print("Successfully retrieved issue!")

    return {
        "summary": summary,
        "description": description,
        "story_points": story_points,
        "acceptance_criteria": acceptance_criteria,
        "epic_link": epic_link,
    }


def update_fields_for_jira_issue(issue_key, data):
    """
    Update specific fields for a Jira issue and return as a dict.
    """
    headers = create_jira_headers(ATLASSIAN_API_TOKEN)
    issue_url = build_board_issue_url_v2(JIRA_BASE_URL, issue_key)

    response = put_board_issues(issue_url, headers, data)
    extract_fields_from_response(response)
    return {"message": "Successfully updated issue!"}


def create_fields_for_jira_issue_comments(issue_key, data):
    """
    Post specific comments for a Jira issue and return as a dict.
    """
    headers = create_jira_headers(ATLASSIAN_API_TOKEN)
    issue_url = build_board_issue_url_v2(JIRA_BASE_URL, issue_key)
    issue_url = issue_url + "/comment"

    response = post_board_issues_comments(issue_url, headers, data)
    fields = extract_fields_from_response(response)
    return fields


def check_status():
    """Check the health of PostgreSQL and Redis services."""

    try:
        conn = psycopg2.connect(database_url)
        conn.close()

        r = redis.Redis.from_url(redis_url)
        r.ping()
    except Exception as e:
        raise InternalServerError(f"connection error: {e}")

    return {
        "database": "connected",
        "cache": "connected",
        "message": "All systems operational",
    }
