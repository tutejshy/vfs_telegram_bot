from sqlalchemy import Column, Integer, String, Boolean

from app.models.domain.base_db import BaseDB


class AccountDB(BaseDB):
    account_id = Column(Integer, primary_key=True, unique=True, index=True)
    actor_id = Column(String(128), unique=True, index=True)
    is_active = Column(Boolean, default=True)
