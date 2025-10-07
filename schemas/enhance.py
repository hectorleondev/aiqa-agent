from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EnhanceCreateRequest(BaseModel):
    issue_key: str


class EnhanceGetRequest(BaseModel):
    message_id: int


class EnhanceResponse(EnhanceCreateRequest):
    id: int
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None
