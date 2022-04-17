from sqlalchemy import Column, Integer, String, DateTime, func

from app.models.domain.base_db import BaseDB


class ActionDB(BaseDB):
    action_id = Column(Integer, primary_key=True, unique=True, index=True)
    login_id = Column(Integer)
    url = Column(String(256))
    client_headers = Column(String)
    server_headers = Column(String)
    response = Column(String)
    http_code = Column(Integer)
    action_at = Column(DateTime(timezone=True), server_default=func.now())
    error = Column(String)
