from sqlalchemy import Column, Integer, String, DateTime, func

from app.models.domain.base_db import BaseDB


class CheatActionDB(BaseDB):
    cheat_action_id = Column(Integer, primary_key=True, unique=True, index=True)
    actor_id = Column(String(128), unique=True, index=True)
    cheat_at = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String)
