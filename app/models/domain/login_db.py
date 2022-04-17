import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, Enum

from app.models.domain.base_db import BaseDB


class LoginStatus(enum.Enum):
    NORMAL = 'normal'
    BUSY = 'busy'
    BLOCK = 'block'


class LoginDB(BaseDB):
    login_id = Column(Integer, primary_key=True, unique=True, index=True)
    login = Column(String(128), unique=True, index=True)
    pwd = Column(String(128))
    route = Column(String(56))
    to = Column(String(8))

    token = Column(String(4096))

    status = Column(Enum(LoginStatus), default=LoginStatus.NORMAL)

    login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now)

    http_code = Column(Integer)
    error_count = Column(Integer)
