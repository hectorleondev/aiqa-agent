
---

# AI QA Agent

This repository contains a Python FastAPI web application for retrieving Jira issue fields via a REST API. The project follows [PEP 8](https://peps.python.org/pep-0008/) style guidelines.

## Features

- **Health Check Endpoint**: `/` returns service status and current time.
- **Jira Fields Endpoint**: `/jira-fields/{issue_key}` fetches summary, description, story points, acceptance criteria, and epic link for a given Jira issue.
- **Error Handling**: Returns appropriate error messages and status codes for not found, unauthorized, and internal errors.

## Setup Instructions

1. **Clone the repository** and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**:  
   Create a `.env` file in the project root with:
    ```
    ATLASSIAN_API_TOKEN=your_jira_api_token
    JIRA_BASE_URL=your_jira_base_url
    ```

3. **Run the application**:
    ```bash
    uvicorn main:app --reload
    ```

4. **Access the API**:
    - Health check: [http://localhost:8000/](http://localhost:8000/)
    - Jira fields: [http://localhost:8000/jira-fields/{issue_key}](http://localhost:8000/jira-fields/{issue_key})
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)


### Run Locally using Docker

1. Install Docker Desktop.

2. Clone the repository

3. **Environment Variables**:  
   Create a `.env` file in the project root with:
    ```
    ATLASSIAN_API_TOKEN=your_jira_api_token
    JIRA_BASE_URL=your_jira_base_url
    ```

4. Run the commands below:
    ```bash
    cd .devcontainer
    docker compose down
    docker compose up --build
    ```

5. **Access the API**:
    - Health check: [http://localhost:8000/](http://localhost:8000/)
    - Jira fields: [http://localhost:8000/jira-fields/{issue_key}](http://localhost:8000/jira-fields/{issue_key})
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)


### Deployment

4. Run the commands below:
    ```bash
    docker build --no-cache --platform linux/amd64 -f deployment/Dockerfile.production -t aiqa-agent-app:latest .
    
    # 3. Get ECR info
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --region us-east-2)
    ECR_URI="${ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/aiqa-agent-app"
    
    # 4. Tag and push
    docker tag aiqa-agent-app:latest ${ECR_URI}:latest
    docker push ${ECR_URI}:latest
    ```

## Testing

- Tests are located in `test_main.py`.
- Run tests with:
    ```bash
    pytest
    ```

- Ensure Docker is installed for Dev Container support.
- Configure Python type checking and inlay hints in VS Code:
  - Set `Python > Analysis > Type Checking Mode` to `basic`
  - Enable `Python > Analysis > Inlay Hints > Function Return Types`
  - Enable `Python > Analysis > Inlay Hints > Variable Types`
- Dev Containers
- Python
- Python Debugger
- Pylance

## Notes

- Ensure Docker is installed for Dev Container support.
- Configure Python type checking and inlay hints in VS Code for better development experience.

---

Replace placeholder values in `.env` with your actual Jira credentials.