from fastapi import APIRouter, Depends
from services.health_service import HealthService
from schemas.health import HealthCheckResponse, SystemStatusResponse
from api.dependencies import get_health_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthCheckResponse, status_code=200)
async def health_check(
    health_service: HealthService = Depends(get_health_service),
) -> HealthCheckResponse:
    """
    Simple health check endpoint.

    Returns:
        HealthCheckResponse: Status information including health status,
                            message, and current timestamp.
    """
    return health_service.get_health_check()


@router.get("/cache-status", response_model=SystemStatusResponse, status_code=200)
async def cache_status(
    health_service: HealthService = Depends(get_health_service),
) -> SystemStatusResponse:
    """
    Detailed system status check.

    Checks connectivity to:
    - PostgreSQL database
    - Redis cache
    - SQS queue configuration

    Returns:
        SystemStatusResponse: Detailed status of all system dependencies.

    Raises:
        500: If any system dependency is unavailable.
    """
    return health_service.get_system_status()
