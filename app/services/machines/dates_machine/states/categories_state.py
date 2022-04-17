from random import randrange
from time import sleep
from typing import Optional, List, Any

import requests
from cloudscraper import CloudScraper

from app.core.uri_v1 import URIv1
from app.models.schema.action_schema import ActionCreate
from app.models.schema.category_schema import Category
from app.models.schema.center_schema import Center
from app.models.schema.login_schema import Login
from app.repo.category_repo import CategoryRepo
from app.repo.center_repo import CenterRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND, CATEGORIES_NOT_FOUND, CENTERS_NOT_FOUND
from app.services.machines.state_machine import State, Transition, ErrorState
from app.util.util import make_client_headers, make_action, parse_categories, sleep_exec


class CategoriesState(State):

    def __init__(self, center_repo: CenterRepo, category_repo: CategoryRepo):
        self._center_repo = center_repo
        self._category_repo = category_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = args if isinstance(args, Login) else None
        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        centers = self._center_repo.fetch_centers_by(login.route)
        if not centers:
            return Transition(ref=DateCheck.RELEASE_RESOURCES, data=login, error=CENTERS_NOT_FOUND)

        actions = self.__load_all_categories(session, login, centers)

        return Transition(ref=DateCheck.DATES, action=actions, data=login)

    def __load_all_categories(self, session: Optional[requests.Session], login: Login, centers: List[Center]) -> List[ActionCreate]:
        actions = []
        for center in centers:
            if not self._category_repo.contains_categories(login.route, center.code):
                actions.append(self.__load_categories(session, login, center.code))
            parents = self._category_repo.fetch_categories_by(login.route, center.code, None)
            for parent in parents:
                if not self._category_repo.contains_categories(login.route, center.code, parent.code):
                    actions.append(self.__load_categories(session, login, center.code, parent.code))

        return actions

    def __load_categories(self, session: Optional[requests.Session], login: Login, center_code: str, parent: Optional[str]=None) -> ActionCreate:
        sleep_exec()

        url = URIv1.categories(to=login.to, center=center_code, parent_category=parent)

        response = session.get(url)

        if response.status_code == 200:
            data = response.json()
            categories = parse_categories(data if isinstance(data, List) else [], parent)
            if categories:
                self._category_repo.merge(login.route, categories)

        return make_action(response, login.login_id)
