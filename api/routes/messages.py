from fastapi import APIRouter, Depends, HTTPException
from repositories.message_repository import MessageRepository
from schemas.message import MessageCreate, MessageResponse, MessageUpdate
from api.dependencies import get_message_repository
from typing import List

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageResponse, status_code=201)
def create_message(
    message: MessageCreate,
    repo: MessageRepository = Depends(get_message_repository)
):
    """Create a new message"""
    return repo.create(
        issue_key=message.issue_key,
        body=message.body,
        status=message.status
    )


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: int,
    repo: MessageRepository = Depends(get_message_repository)
):
    """Get message by ID"""
    message = repo.get_by_id(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.get("/issue/{issue_key}", response_model=List[MessageResponse])
def get_messages_by_issue(
    issue_key: str,
    repo: MessageRepository = Depends(get_message_repository)
):
    """Get all messages for a specific issue"""
    return repo.get_by_issue_key(issue_key)


@router.patch("/{message_id}", response_model=MessageResponse)
def update_message_status(
    message_id: int,
    update: MessageUpdate,
    repo: MessageRepository = Depends(get_message_repository)
):
    """Update message status"""
    message = repo.update_status(message_id, update.status)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message