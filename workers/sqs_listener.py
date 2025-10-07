import time
import signal
import logging
from fastapi import Depends
from core.config import get_settings
from repositories.sqs_repository import SQSRepository
from services.sqs_processor_service import SQSProcessorService
from sqlalchemy.orm import Session
from db.session import get_db
from repositories.message_repository import MessageRepository



# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SQSListener:
    def __init__(self):
        self.running = True
        self.settings = get_settings()
        self.db_session: Session = Depends(get_db)

        # Initialize repositories
        self.sqs_repo = SQSRepository(self.settings)
        self.message_repo = MessageRepository(self.db_session)

        # Initialize services
        self.processor = SQSProcessorService(self.sqs_repo, self.message_repo)

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    def start(self):
        """Start listening for SQS messages"""
        logger.info(f"Starting SQS listener for queue: {self.settings.sqs_queue_url}")
        logger.info("Waiting for messages... (Press Ctrl+C to stop)")

        consecutive_empty_receives = 0
        max_empty_receives = 3

        while self.running:
            try:
                # Receive messages (long polling)
                messages = self.sqs_repo.receive_messages(
                    max_messages=10, wait_time_seconds=20  # Long polling
                )

                if not messages:
                    consecutive_empty_receives += 1
                    if consecutive_empty_receives >= max_empty_receives:
                        logger.debug("No messages received, continuing to poll...")
                        consecutive_empty_receives = 0
                    continue

                consecutive_empty_receives = 0
                logger.info(f"Received {len(messages)} message(s)")

                # Process each message
                for message in messages:
                    if not self.running:
                        break

                    success = self.processor.process_message(message)

                    if not success:
                        logger.warning(
                            f"Failed to process message: {message.get('MessageId')}"
                        )

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
                break

            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(5)  # Wait before retrying

        logger.info("SQS listener stopped")


def main():
    """Main entry point"""
    listener = SQSListener()
    listener.start()


if __name__ == "__main__":
    main()
