from typing import Any, Optional

from app.repo.action_repo import ActionRepo
from app.repo.category_repo import CategoryRepo
from app.repo.center_repo import CenterRepo
from app.repo.login_repo import LoginRepo
from app.repo.post_repo import PostRepo
from app.services.machines.dates_machine.states.release_resources_state import ReleaseResourcesState
from app.services.machines.state_machine import ErrorState


class StateFactory:
    def __init__(self, login_repo: LoginRepo,
                 center_repo: CenterRepo,
                 category_repo: CategoryRepo,
                 post_repo: PostRepo,
                 action_repo: ActionRepo):

        self._login_repo = login_repo
        self._center_repo = center_repo
        self._category_repo = category_repo
        self._post_repo = post_repo
        self._action_repo = action_repo

    def of(self, ref: Any, args: Optional[Any] = None) -> Optional[Any]:
        from app.services.machines.categories_machine.category_check_states import CategoryCheck

        if CategoryCheck.CENTERS == ref:
            from app.services.machines.categories_machine.states.centers_state import CentersState
            return CentersState(center_repo=self._center_repo, login_repo=self._login_repo)
        if CategoryCheck.CATEGORIES == ref:
            from app.services.machines.categories_machine.states.categories_state import CategoriesState
            return CategoriesState(center_repo=self._center_repo, category_repo=self._category_repo)
        if CategoryCheck.TERMINATE == ref:
            return None

        from app.services.machines.dates_machine.date_check_states import DateCheck

        if DateCheck.FIND_LOGIN == ref:
            from app.services.machines.dates_machine.states.find_login_state import FindLoginState
            return FindLoginState(login_repo=self._login_repo)
        if DateCheck.LOGIN == ref:
            from app.services.machines.dates_machine.states.login_state import LoginState
            return LoginState(login_repo=self._login_repo)
        if DateCheck.CENTERS == ref:
            from app.services.machines.dates_machine.states.centers_state import CentersState
            return CentersState(center_repo=self._center_repo)
        if DateCheck.CATEGORIES == ref:
            from app.services.machines.dates_machine.states.categories_state import CategoriesState
            return CategoriesState(center_repo=self._center_repo, category_repo=self._category_repo)
        if DateCheck.DATES == ref:
            from app.services.machines.dates_machine.states.dates_state import DatesState
            return DatesState(center_repo=self._center_repo, category_repo=self._category_repo, post_repo=self._post_repo)
        if DateCheck.RELEASE_RESOURCES == ref:
            return ReleaseResourcesState(login_repo=self._login_repo, last_error=args if isinstance(args, ErrorState) else None)

        return None
