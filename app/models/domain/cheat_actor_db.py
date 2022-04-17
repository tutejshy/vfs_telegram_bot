from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from app.models.domain.base_db import BaseDB


class CheatActorDB(BaseDB):
    cheat_actor_id = Column(Integer, primary_key=True, unique=True, index=True)
    actor_id = Column(String(128), unique=True, index=True)
    cheat_count = Column(Integer, default=0)
    last_cheat_at = Column(DateTime(timezone=True), server_default=func.now())
