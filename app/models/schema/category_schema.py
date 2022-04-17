from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Category(BaseModel):
    code: str = Field(...)
    mission_code: str = Field(...)
    parent: Optional[str]
    name: Optional[str]
    center: Optional[str]
