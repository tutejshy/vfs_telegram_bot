from typing import Optional, Any, List

from app.services.machines.state_factory import StateFactory

from app.models.schema.action_schema import ActionCreate
from app.repo.action_repo import ActionRepo
from app.services.machines.categories_machine.category_check_states import CategoryCheck


from app.services.machines.state_machine import StateMachine


class CategoryCheckingMachine(StateMachine):

    def __init__(self, factory: StateFactory, action_repo: ActionRepo):
        super().__init__(CategoryCheck.CENTERS)
        self._factory = factory
        self._action_repo = action_repo

    def _create_state(self, ref: Any, args: Optional[Any] = None) -> Optional[Any]:
        return self._factory.of(ref, args)

    def _add_action(self, action: Optional[Any]):
        if isinstance(action, ActionCreate):
            self._action_repo.create(action)
        elif isinstance(action, List):
            for item in action:
                self._add_action(item)
