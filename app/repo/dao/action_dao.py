from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.models.domain.base import ActionDB
from app.models.schema.action_schema import ActionCreate


class ActionDao:
    @staticmethod
    def fetch_all(db: Session) -> List[ActionDB]:
        return db.query(ActionDB).all()

    @staticmethod
    def create(db: Session, action: ActionCreate) -> ActionDB:
        model = ActionDB()

        model.login_id = action.login_id
        model.url = action.url
        model.client_headers = action.client_headers
        model.server_headers = action.server_headers
        model.response = action.response
        model.http_code = action.http_code
        model.action_at = action.action_at or datetime.now()
        model.error = action.error

        db.add(model)

        return model
