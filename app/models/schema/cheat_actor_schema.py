from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel


class CheatActor(BaseModel):
    actor_id: str = Field(...)
    cheat_count: int
    last_cheat_at: datetime


class CheatAction(BaseModel):
    actor_id: str = Field(...)
    cheat_at: datetime
    action: str
