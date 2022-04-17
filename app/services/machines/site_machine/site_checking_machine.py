from typing import Optional, Any, List

from app.models.schema.action_schema import ActionCreate
from app.repo.action_repo import ActionRepo
from app.services.machines.site_machine.site_check_states import SiteCheck
from app.services.machines.state_machine import StateMachine, Transition


class SiteCheckingMachine(StateMachine):
    def __init__(self, action_repo: ActionRepo):
        super().__init__(SiteCheck.TERMINATE, )
        self._action_repo = action_repo

    def _create_state(self, ref: Any, args: Optional[Any] = None) -> Optional[Any]:
        return None

    def _add_action(self, action: Optional[Any]):
        if isinstance(action, ActionCreate):
            self._action_repo.create(action)
        elif isinstance(action, List):
            for item in action:
                self._add_action(item)
