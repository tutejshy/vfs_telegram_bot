from enum import Enum
from typing import Any, Optional

from app.repo.action_repo import ActionRepo
from app.services.machines.state_factory import StateFactory


class Machine(Enum):
    SITE = "site"
    DICTIONARY = "category"
    DATES = "dates"


class MachineFactory:
    def __init__(self, state_factory: StateFactory, action_repo: ActionRepo):
        self._state_factory = state_factory
        self._action_repo = action_repo

    def of(self, ref: Any) -> Optional[Any]:
        if Machine.SITE == ref:
            from app.services.machines.site_machine.site_checking_machine import SiteCheckingMachine
            return SiteCheckingMachine(self._action_repo)
        if Machine.DICTIONARY == ref:
            from app.services.machines.categories_machine.category_checking_machine import CategoryCheckingMachine
            return CategoryCheckingMachine(self._state_factory, self._action_repo)
        if Machine.DATES == ref:
            from app.services.machines.dates_machine.date_checking_machine import DateCheckingMachine
            return DateCheckingMachine(self._state_factory, self._action_repo)
        return None
