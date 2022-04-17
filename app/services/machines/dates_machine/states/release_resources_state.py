from typing import Optional, Any

from cloudscraper import CloudScraper

from app.models.domain.login_db import LoginStatus
from app.models.schema.login_schema import Login
from app.repo.login_repo import LoginRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND
from app.services.machines.state_machine import State, Transition


class ReleaseResourcesState(State):

    def __init__(self, login_repo: LoginRepo, last_error: Optional[Any]):
        self._login_repo = login_repo
        self._last_error = last_error

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = args if isinstance(args, Login) else None

        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        if isinstance(login, Login):
            login.status = LoginStatus.NORMAL
            self._login_repo.update_login(login)

        return Transition(ref=DateCheck.TERMINATE, data=login, error=self._last_error)
