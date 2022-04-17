from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Center(BaseModel):
    code: str = Field(...)
    name: Optional[str]
