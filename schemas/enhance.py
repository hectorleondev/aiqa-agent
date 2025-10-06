from pydantic import BaseModel


class EnhanceCreate(BaseModel):
    issue_key: str


class EnhanceGet(BaseModel):
    id: int
