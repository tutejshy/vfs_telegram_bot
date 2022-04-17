from typing import Optional, Any

from cloudscraper import CloudScraper

from app.core.uri_v1 import URIv1
from app.models.schema.login_schema import Login
from app.repo.login_repo import LoginRepo
from app.services.machines.dates_machine.date_check_states import DateCheck
from app.services.machines.errors.error import LOGIN_NOT_FOUND
from app.services.machines.state_machine import State, Transition, ErrorState
from app.util.util import make_action


class LoginState(State):

    def __init__(self, login_repo: LoginRepo):
        self._login_repo = login_repo

    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        login = args if isinstance(args, Login) else None
        if not login:
            return Transition(ref=DateCheck.TERMINATE, error=LOGIN_NOT_FOUND)

        url = URIv1.login()

        params = self.__make_params(login)
        headers = self.__make_headers()

        response = session.post(url, params=params, headers=headers)

        action = make_action(response, login.login_id)
        login.http_code = response.status_code

        next_state = DateCheck.CENTERS
        error = None
        if response.status_code == 200:
            token = self.__get_safe_access_token(response.json())
            if token:
                login.token = token
            else:
                next_state = DateCheck.RELEASE_RESOURCES
                error = ErrorState()
        else:
            next_state = DateCheck.RELEASE_RESOURCES
            error = ErrorState()

        return Transition(ref=next_state, data=login, action=action, error=error)

    @staticmethod
    def __get_safe_access_token(json) -> Optional[str]:
        return json.get("accessToken") if json else None

    @staticmethod
    def __make_params(login: Login):
        return {
            "username": login.login,
            "password": login.pwd,
            "missioncode": login.to,
            "countrycode": "blr"
        }

    @staticmethod
    def __make_headers():
        return {"content-type": "application/x-www-form-urlencoded"}
