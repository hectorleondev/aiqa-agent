import boto3
import json
from typing import List, Dict, Optional
from core.config import Settings
from core.exceptions import InternalServerError


class SQSRepository:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.sqs_client = boto3.client(
            "sqs",
            region_name=settings.aws_region
            if hasattr(settings, "aws_region")
            else "us-east-1",
        )
        self.queue_url = settings.sqs_queue_url

    def receive_messages(
        self,
        max_messages: int = 10,
        wait_time_seconds: int = 20,
        visibility_timeout: int = 30,
    ) -> List[Dict]:
        """
        Receive messages from SQS queue using long polling.

        Args:
            max_messages: Max number of messages to receive (1-10)
            wait_time_seconds: Long polling wait time (0-20 seconds)
            visibility_timeout: How long message is hidden from other consumers

        Returns:
            List of messages
        """
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time_seconds,
                VisibilityTimeout=visibility_timeout,
                MessageAttributeNames=["All"],
                AttributeNames=["All"],
            )

            return response.get("Messages", [])

        except Exception as e:
            raise InternalServerError(f"Failed to receive SQS messages: {str(e)}")

    def delete_message(self, receipt_handle: str) -> None:
        """Delete a message after successful processing"""
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
            )
        except Exception as e:
            raise InternalServerError(f"Failed to delete SQS message: {str(e)}")

    def change_message_visibility(
        self, receipt_handle: str, visibility_timeout: int
    ) -> None:
        """Change message visibility timeout (for extending processing time)"""
        try:
            self.sqs_client.change_message_visibility(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle,
                VisibilityTimeout=visibility_timeout,
            )
        except Exception as e:
            raise InternalServerError(f"Failed to change message visibility: {str(e)}")

    def send_message(self, message_body: Dict) -> Dict:
        """Send a message to the queue"""
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url, MessageBody=json.dumps(message_body)
            )
            return response
        except Exception as e:
            raise InternalServerError(f"Failed to send SQS message: {str(e)}")
