import datetime
from random import randrange
from time import sleep
from typing import Optional, List, Callable, Any

import requests
from cloudscraper import CloudScraper

from app.core.uri_v1 import URIv1
from app.models.domain.login_db import LoginStatus
from app.models.schema.action_schema import ActionCreate
from app.models.schema.category_schema import Category
from app.models.schema.login_schema import Login
from app.models.schema.post_schema import PostCreate
from app.repo.category_repo import CategoryRepo
from app.repo.center_repo import CenterRepo
from app.repo.post_repo import PostRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND
from app.services.machines.state_machine import State, Transition
from app.util.util import make_client_headers, make_action, parse_dates, dates_to_formatted_message, sleep_exec


class DatesState(State):

    def __init__(self, center_repo: CenterRepo, category_repo: CategoryRepo, post_repo: PostRepo):
        self._center_repo = center_repo
        self._category_repo = category_repo
        self._post_repo = post_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = args if isinstance(args, Login) else None
        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        centers = self._center_repo.fetch_centers_by(login.route)
        actions = []
        for center in centers:
            parents = self._category_repo.fetch_root_categories_by(login.route, center.code)
            for parent in parents:
                children = self._category_repo.fetch_categories_by(login.route, center.code, parent.code)
                for child in children:
                    actions.append(self.__load_dates(session, login, child))

        return Transition(ref=DateCheck.RELEASE_RESOURCES, action=actions, data=login)

    def __load_dates(self, session: Optional[requests.Session], login: Login, category: Category) -> ActionCreate:
        sleep_exec()

        headers = self.__make_headers(login)
        url = self.__make_url(login.login, category)

        response = session.get(url, headers=headers)

        login.http_code = response.status_code
        if response.status_code == 200:
            data = response.json()
            dates = parse_dates(data if isinstance(data, List) else [])
            message = dates_to_formatted_message(dates)
            if message:
                self._post_repo.merge(self.__make_post(login.route, message))
        return make_action(response, login.login_id)

    @staticmethod
    def __make_url(login: str, category: Category) -> str:
        return URIv1.slots(login_email=login,
                           mission_code=category.mission_code,
                           center_code=category.center,
                           visa_code=category.code)

    @staticmethod
    def __make_headers(login: Login):
        headers = make_client_headers(login, use_auth=True)
        return headers

    @staticmethod
    def __make_post(route: str, message: str) -> PostCreate:
        return PostCreate(route=route, message=message)
