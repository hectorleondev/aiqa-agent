import json
import logging
from typing import Dict
from repositories.sqs_repository import SQSRepository
from repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)


class EnhanceService:
    def __init__(self, sqs_repo: SQSRepository, message_repo: MessageRepository):
        self.sqs_repo = sqs_repo
        self.message_repo = message_repo

    def create_jira_stories_enhance(self, issue_key: str, wait_seconds: int):
        db_message = self.message_repo.create(
            issue_key=issue_key, body="", status="in_progress"
        )
        self.sqs_repo.send_message(
            {"message_id": db_message.id, "wait_seconds": wait_seconds}
        )
        return db_message
