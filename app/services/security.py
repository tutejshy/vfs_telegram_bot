from typing import Optional, List

from app.repo.account_repo import AccountRepo
from app.repo.cheat_repo import CheatRepo
from app.util.util import call_stack


class Security:
    def __init__(self, bot_login: str, bot_password: str, account_repo: AccountRepo, cheat_repo: CheatRepo):
        self._bot_login = bot_login
        self._bot_password = bot_password
        self._account_repo = account_repo
        self._cheat_repo = cheat_repo

    def login(self, actor_id: str, args: Optional[List[str]]) -> bool:
        if args and len(args) == 2 and self._check(actor_id, args[0], args[1]):
            self._account_repo.auth(actor_id)
            return True

        self._cheat_repo.cheat_action(actor_id, call_stack())
        return False

    def logged_in(self, actor_id: str) -> bool:
        if not self._account_repo.logged_in(actor_id):
            self._cheat_repo.cheat_action(actor_id, call_stack())
            return False
        return True

    def _auth(self, actor_id: str):
        self._account_repo.auth(actor_id)

    def _check(self, actor_id: str, user: str, pwd: str) -> bool:
        return not self._cheat_repo.is_blocked(actor_id) and self._bot_login == user and self._bot_login == pwd
