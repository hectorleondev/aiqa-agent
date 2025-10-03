import json
import logging
from typing import Dict
from repositories.sqs_repository import SQSRepository
from repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)


class SQSProcessorService:
    def __init__(self, sqs_repo: SQSRepository, message_repo: MessageRepository ):
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
            message_id = message.get("MessageId")
            receipt_handle = message.get("ReceiptHandle")

            # Store message in database
            db_message = self.message_repo.create(
                issue_key=body.get('issue_key'),
                body=json.dumps(body),
                status="processing"
            )

            logger.info(f"Processing message {message_id}: {body}")

            self.message_repo.update_status(db_message.id, "completed")

            # Delete message after successful processing
            self.sqs_repo.delete_message(receipt_handle)
            logger.info(f"Successfully processed and deleted message {message_id}")

            return True

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in message: {e}")
            # Delete malformed messages
            self.sqs_repo.delete_message(message.get("ReceiptHandle"))
            return False

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return False
