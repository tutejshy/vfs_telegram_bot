import sys
from random import randrange
from time import sleep
from typing import Optional, List, Any

import requests
from cloudscraper import CloudScraper
from dependency_injector.wiring import Provide, inject

from app.core.uri_v1 import URIv1
from app.models.schema.action_schema import ActionCreate
from app.models.schema.center_schema import Center
from app.repo.category_repo import CategoryRepo
from app.repo.center_repo import CenterRepo
from app.services.machines.categories_machine.category_check_states import CategoryCheck
from app.services.machines.errors.error import CENTERS_NOT_FOUND, ARGS_NOT_FOUND
from app.services.machines.state_machine import State, Transition, ErrorState
from app.util.util import make_action, parse_categories, sleep_exec


class CategoriesState(State):
    def __init__(self, center_repo: CenterRepo, category_repo: CategoryRepo):
        self._center_repo = center_repo
        self._category_repo = category_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        routes = args.get("routes") if args else None
        if not routes:
            return Transition(ref=CategoryCheck.TERMINATE, error=ARGS_NOT_FOUND)

        all_actions = []
        for item in routes:
            centers = self._center_repo.fetch_centers_by(item.route)
            actions = self.__load_all_categories(session, item.route, item.to, centers)
            all_actions.extend(actions)

        return Transition(ref=CategoryCheck.TERMINATE, action=all_actions)

    def __load_all_categories(self, session: Optional[CloudScraper], route: str, to: str, centers: List[Center]) -> List[ActionCreate]:
        actions = []
        for center in centers:
            if not self._category_repo.contains_categories(route, center.code):
                actions.append(self.__load_categories(session, route, to, center.code))

            parents = self._category_repo.fetch_categories_by(route, center.code, None)
            for parent in parents:
                if not self._category_repo.contains_categories(route, center.code, parent.code):
                    actions.append(self.__load_categories(session, route, to, center.code, parent.code))
        return actions

    def __load_categories(self, session: Optional[CloudScraper], route: str, to: str, center_code: str, parent: Optional[str]=None) -> ActionCreate:
        sleep_exec()
        url = URIv1.categories(to=to, center=center_code, parent_category=parent)

        response = session.get(url)

        if response.status_code == 200:
            data = response.json()
            categories = parse_categories(data if isinstance(data, List) else [], parent)
            self._category_repo.merge(route, categories)

        return make_action(response)
