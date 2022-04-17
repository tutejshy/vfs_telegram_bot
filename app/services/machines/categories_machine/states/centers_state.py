from typing import Optional, List, Any

from cloudscraper import CloudScraper

from app.core.uri_v1 import URIv1
from app.models.schema.action_schema import ActionCreate
from app.repo.center_repo import CenterRepo
from app.repo.login_repo import LoginRepo
from app.services.machines.categories_machine.category_check_states import CategoryCheck
from app.services.machines.errors.error import ARGS_NOT_FOUND
from app.services.machines.state_machine import State, Transition
from app.util.util import make_action, parse_centers, sleep_exec


class CentersState(State):
    def __init__(self, center_repo: CenterRepo, login_repo: LoginRepo):
        self._center_repo = center_repo
        self._login_repo = login_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        routes = self._login_repo.get_available_routes()
        if not routes:
            return Transition(ref=CategoryCheck.TERMINATE, error=ARGS_NOT_FOUND)

        actions = []
        for item in routes:
            if self._center_repo.get_number_of_centers(item.route) == 0:
                action = self.__load_centers(session, item.route, item.to)
                actions.append(action)

        return Transition(ref=CategoryCheck.CATEGORIES, action=actions, data={"routes": routes})

    def __load_centers(self, session: Optional[CloudScraper], route: str, to: str) -> ActionCreate:
        sleep_exec()
        url = URIv1.centers(to)

        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            centers = parse_centers(data if isinstance(data, List) else [])
            self._center_repo.merge(route, centers)

        return make_action(response)
