import json
import logging
from typing import Dict
from repositories.sqs_repository import SQSRepository

logger = logging.getLogger(__name__)


class SQSProcessorService:
    def __init__(self, sqs_repo: SQSRepository):
        self.sqs_repo = sqs_repo

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

            logger.info(f"Processing message {message_id}: {body}")

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
