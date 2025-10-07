from fastapi import APIRouter, Depends
from services.enhance_service import EnhanceService
from schemas.enhance import EnhanceCreateRequest, EnhanceGetRequest, EnhanceResponse
from api.dependencies import get_enhance_service

router = APIRouter(prefix="/jira/stories/enhance", tags=["Jira Enhance"])


@router.post("/", response_model=EnhanceResponse)
async def create_jira_enhance(
    request: EnhanceCreateRequest,
    enhance_service: EnhanceService = Depends(get_enhance_service),
):
    """Create a comment on a Jira issue"""
    return enhance_service.create_jira_stories_enhance(request.issue_key, 30)


@router.get("/status/{id}", response_model=EnhanceResponse)
def get_message(
    id: int, enhance_service: EnhanceService = Depends(get_enhance_service)
):
    """Get message by ID"""
    return enhance_service.get_jira_stories_enhance(id)
