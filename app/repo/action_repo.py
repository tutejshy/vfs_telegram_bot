from datetime import datetime
from typing import Optional

from app.models.schema.action_schema import ActionCreate
from app.repo.base_repo import BaseRepo
from app.repo.dao.action_dao import ActionDao


class ActionRepo(BaseRepo):

    def create(self, login_id: Optional[int], url: str,
               client_headers: Optional[str] = None,
               server_headers: Optional[str] = None,
               response: Optional[str] = None,
               http_code: Optional[int] = None,
               action_at: Optional[datetime] = datetime.now(),
               error: Optional[str] = None):
        db = self._db()
        ActionDao.create(db, ActionCreate(login_id=login_id,
                                          url=url,
                                          client_headers=client_headers,
                                          server_headers=server_headers,
                                          response=response,
                                          http_code=http_code,
                                          action_at=action_at,
                                          error=error))
        db.commit()

    def create(self, action: ActionCreate):
        db = self._db()
        ActionDao.create(db, action)
        db.commit()
