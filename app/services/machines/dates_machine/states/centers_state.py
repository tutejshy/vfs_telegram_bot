from typing import Optional, List, Any

import requests
from cloudscraper import CloudScraper

from app.core.uri_v1 import URIv1
from app.models.domain.login_db import LoginStatus
from app.models.schema.login_schema import Login
from app.repo.center_repo import CenterRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND, CENTERS_NOT_FOUND
from app.services.machines.state_machine import State, Transition, ErrorState
from app.util.util import make_client_headers, make_action, parse_centers


class CentersState(State):
    def __init__(self, center_repo: CenterRepo):
        self._center_repo = center_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = args if isinstance(args, Login) else None
        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        if self._center_repo.get_number_of_centers(login.route) > 0:
            Transition(ref=DateCheck.CATEGORIES, data=login, action=None)

        url = URIv1.centers(login.to)

        response = session.get(url)

        action = make_action(response, login.login_id)

        if response.status_code == 200:
            data = response.json()
            centers = parse_centers(data if isinstance(data, List) else [])
            if centers:
                self._center_repo.merge(login.route, centers)
                return Transition(ref=DateCheck.CATEGORIES, data=login, action=action)

        return Transition(ref=DateCheck.RELEASE_RESOURCES, data=login, action=action, error=CENTERS_NOT_FOUND)


