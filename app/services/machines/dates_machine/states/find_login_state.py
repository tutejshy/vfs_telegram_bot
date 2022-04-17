from typing import Optional, Any

import requests
from cloudscraper import CloudScraper

from app.models.domain.login_db import LoginStatus
from app.models.schema.login_schema import Login
from app.repo.login_repo import LoginRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND
from app.services.machines.state_machine import State, Transition, ErrorState
from app.util.util import make_client_headers, make_action


class FindLoginState(State):

    def __init__(self, login_repo: LoginRepo):
        self._login_repo = login_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = self._login_repo.get_available_login()
        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        login.status = LoginStatus.BUSY
        self._login_repo.update_login(login)

        return Transition(ref=DateCheck.LOGIN, data=login)
