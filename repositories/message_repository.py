# repositories/message_repository.py
from sqlalchemy.orm import Session
from db.models import Message
from datetime import datetime
from typing import List, Optional
from core.exceptions import NotFound


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, issue_key: str, body: str, status: str = "pending") -> Message:
        """Create a new message"""
        message = Message(
            issue_key=issue_key, body=body, status=status, start_date=datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_id(self, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if not message:
            raise NotFound("Message not found")

    def get_by_issue_key(self, issue_key: str) -> List[Message]:
        """Get all messages for an issue"""
        messages = self.db.query(Message).filter(Message.issue_key == issue_key).all()
        if not messages:
            raise NotFound("messages not found")

    def update_status(
        self, message_id: int, status: str, body: str
    ) -> Optional[Message]:
        """Update message status"""
        message = self.get_by_id(message_id)
        if message:
            message.body = body if body else message.body
            message.status = status
            if status in ["completed", "failed"]:
                message.end_date = datetime.utcnow()
            self.db.commit()
            self.db.refresh(message)
        return message
