from typing import Optional, Any, Callable, List

from app.models.schema.action_schema import ActionCreate
from app.repo.action_repo import ActionRepo
from app.services.machines.dates_machine.date_check_states import DateCheck

from app.services.machines.state_factory import StateFactory
from app.services.machines.state_machine import StateMachine


class DateCheckingMachine(StateMachine):
    def __init__(self, factory: StateFactory, action_repo: ActionRepo, messanger: Optional[Callable] = None):
        super().__init__(DateCheck.FIND_LOGIN)
        self._factory = factory
        self._action_repo = action_repo
        self._messanger = messanger

    def _create_state(self, ref: Any, args: Optional[Any] = None) -> Optional[Any]:
        return self._factory.of(ref, args)

    def _add_action(self, action: Optional[Any]):
        if isinstance(action, ActionCreate):
            self._action_repo.create(action)
        elif isinstance(action, List):
            for item in action:
                self._add_action(item)
