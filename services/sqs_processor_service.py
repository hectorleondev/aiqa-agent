import json
import logging
import time
from typing import Dict
from repositories.sqs_repository import SQSRepository
from repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)


class SQSProcessorService:
    def __init__(self, sqs_repo: SQSRepository, message_repo: MessageRepository):
        self.sqs_repo = sqs_repo
        self.message_repo = message_repo

    def process_message(self, message: Dict) -> bool:
        """
        Process a single SQS message.

        Returns:
            True if processing succeeded, False otherwise
        """
        try:
            # Parse message body
            body = json.loads(message.get("Body", "{}"))
            sqs_message_id = message.get("MessageId")
            receipt_handle = message.get("ReceiptHandle")
            logger.info(f"Processing sqs message {sqs_message_id}: {body}")

            message_id = body.get("message_id", 0)
            wait_seconds = body.get("wait_seconds", 0)

            time.sleep(wait_seconds)
            self.message_repo.update_status(message_id, "completed", sqs_message_id)

            # Delete message after successful processing
            self.sqs_repo.delete_message(receipt_handle)
            logger.info(f"Successfully processed and deleted message {sqs_message_id}")

            return True

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in message: {e}")
            # Delete malformed messages
            self.sqs_repo.delete_message(message.get("ReceiptHandle"))
            return False

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return False
