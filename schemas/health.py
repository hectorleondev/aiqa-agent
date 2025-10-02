from pydantic import BaseModel
from typing import Optional

class HealthCheckResponse(BaseModel):
    status: str
    message: str
    time: str

class SystemStatusResponse(BaseModel):
    database: str
    cache: str
    sqs_url: str
    message: str
    message: str