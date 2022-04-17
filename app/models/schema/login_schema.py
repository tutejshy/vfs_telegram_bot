from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from app.models.domain.login_db import LoginStatus


class LoginMerge(BaseModel):
    login: str = Field(...)
    pwd: str = Field(...)
    route: str = Field(...)
    to: Optional[str]

    token: Optional[str]
    status: Optional[LoginStatus]

    login_at: Optional[datetime]
    http_code: Optional[int]
    error_count: Optional[int]


class Login(BaseModel):
    login_id: int = Field(...)
    login: str = Field(...)
    pwd: str = Field(...)
    route: str = Field(...)
    to: str = Field(...)

    token: Optional[str]
    status: LoginStatus

    login_at: Optional[datetime]
    http_code: Optional[int]
    error_count: Optional[int]

    class Config:
        orm_mode = True


class Route(BaseModel):
    route: str
    to: str
