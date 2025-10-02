from datetime import datetime
from repositories.health_repository import HealthRepository
from schemas.health import HealthCheckResponse, SystemStatusResponse
from core.config import Settings


class HealthService:
    def __init__(self, health_repo: HealthRepository, settings: Settings):
        self.health_repo = health_repo
        self.settings = settings

    def get_health_check(self) -> HealthCheckResponse:
        """Simple health check endpoint"""
        return HealthCheckResponse(
            status="healthy",
            message=f"{self.settings.app_name} is running smoothly",
            time=datetime.now().isoformat(),
        )

    def get_system_status(self) -> SystemStatusResponse:
        """Detailed system status with dependency checks"""
        # Check database connection
        self.health_repo.check_postgres()

        # Check Redis connection
        self.health_repo.check_redis()

        return SystemStatusResponse(
            database="connected",
            cache="connected",
            sqs_url=self.settings.sqs_queue_url,
            message="All systems operational",
        )
