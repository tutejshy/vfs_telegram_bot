from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActionCreate(BaseModel):
    url: str = Field(...)
    login_id: Optional[int]  # = Field(...)
    client_headers: Optional[str]
    server_headers: Optional[str]
    response: Optional[str]
    http_code: Optional[int]

    action_at: Optional[datetime] = datetime.now()
    error: Optional[str]

    class Config:
        orm_mode = True
