from datetime import datetime
from typing import Optional, List

from app.db.session import DBEngine
from app.models.schema.cheat_actor_schema import CheatActor
from app.repo.base_repo import BaseRepo


class CheatRepo(BaseRepo):
    def __init__(self, engine: DBEngine):
        super().__init__(engine)
        self._cache_cheat: List[CheatActor] = []
        self._cache_size: int = 0

    def is_blocked(self, actor_id: str) -> bool:
        actor = next(filter(lambda i: i.actor_id == actor_id, self._cache_cheat), None)
        return actor.cheat_count >= 10 if actor else False

    def cheat_action(self, actor_id: str, actions: Optional[str]):
        actor = next(filter(lambda i: i.actor_id == actor_id, self._cache_cheat), None)
        if not actor:
            actor = CheatActor(actor_id=actor_id, cheat_count=0, last_cheat_at=datetime.now())
            self._cache_cheat.append(actor)
            self._cache_size += 1
            # save to db

        actor.cheat_count += 1
        actor.last_cheat_at = datetime.now()
        if actor.cheat_count <= 10:
            pass
            # save to db

        print("save suspicious_activity")
