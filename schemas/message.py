from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    issue_key: str
    body: str
    status: str = "pending"


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    status: Optional[str] = None
    body: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True