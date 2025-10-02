
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

4. Push new image to registry:
    ```bash
   
    NEW_VERSION="v1"
   
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --region us-east-1)
    
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
 
    ECR_IMAGE_URI="${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/aiqa-agent-app:${NEW_VERSION}"
      
    docker build --no-cache --platform linux/amd64 -f deployment/Dockerfile.production -t aiqa-agent-app:latest .

    docker tag aiqa-agent-app:latest $ECR_IMAGE_URI
   
    docker push $ECR_IMAGE_URI
    ```

5. Create new stack (first time):
    ```bash
    aws cloudformation create-stack \
      --stack-name aiqa-agent-stack \
      --template-body file://deployment/simple-ec2-deployment.yaml \
      --parameters \
        ParameterKey=InstanceType,ParameterValue=t3.micro \
        ParameterKey=KeyPairName,ParameterValue=aiqa-agent-keypair \
        ParameterKey=ECRImageURI,ParameterValue=$(aws ecr describe-repositories --repository-name aiqa-agent-app --query 'repositories[0].repositoryUri' --output text):${NEW_VERSION} \
        ParameterKey=AllowedCIDR,ParameterValue=0.0.0.0/0 \
        ParameterKey=PostgresPassword,ParameterValue=postgres \
        ParameterKey=RedisPassword,ParameterValue=redis123 \
        ParameterKey=SecretKey,ParameterValue=your-random-secret-key-here \
      --capabilities CAPABILITY_NAMED_IAM

    ```

6. Update stack:
    ```bash
    aws cloudformation update-stack \
      --stack-name aiqa-agent-stack \
      --region us-east-1 \
      --use-previous-template \
      --parameters \
        ParameterKey=ECRImageURI,ParameterValue=$(aws ecr describe-repositories --repository-name aiqa-agent-app --query 'repositories[0].repositoryUri' --output text):${NEW_VERSION} \
        ParameterKey=InstanceType,UsePreviousValue=true \
        ParameterKey=KeyPairName,UsePreviousValue=true \
        ParameterKey=AllowedCIDR,UsePreviousValue=true \
        ParameterKey=PostgresPassword,UsePreviousValue=true \
        ParameterKey=RedisPassword,UsePreviousValue=true \
        ParameterKey=SecretKey,UsePreviousValue=true \
      --capabilities CAPABILITY_NAMED_IAM
    ```

7. Test deployment image locally (optional):
    ```bash
    docker run -d \
      --name aiqa-agent \
      --platform linux/amd64 \
      -p 8000:8000 \
      -e ENVIRONMENT=production \
      -e ATLASSIAN_API_TOKEN="MDY2NDE4MjM5MzYwOnvQog+EG1fhPSdOeKV4/dr6cDKR" \
      -e JIRA_BASE_URL="jira-staging.wgu.edu" \
      -e DATABASE_URL="postgresql://postgres:postgres@host.docker.internal:5432/aiqa_agent" \
      -e REDIS_URL="redis://:redis123@host.docker.internal:6379" \
      -e SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789/your-queue" \
      -e OPEN_API_KEY="test" \
      aiqa-agent-app:latest
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