from abc import ABC
from typing import Optional, Any

import cloudscraper
from cloudscraper import CloudScraper
from pydantic import BaseModel, Field


class ErrorState(BaseModel):
    code: Optional[int]
    message: Optional[str]


class Transition(BaseModel):
    ref: Any = Field(...)
    data: Optional[Any] = None
    action: Optional[Any] = None
    error: Optional[ErrorState] = None


class State:
    def run(self, session: Optional[CloudScraper], args: Optional[Any]) -> Transition:
        pass


class StateMachine(ABC):

    def __init__(self, start_state: Any):
        self._start_state = start_state

    def exec(self) -> bool:
        session = cloudscraper.create_scraper(delay=100, debug=True)
        transition = None
        state = self.next_state(self._start_state)
        while state:
            transition = state.run(session=session, args=transition.data if transition else None)
            self._save_action(transition)
            state = self.next_state(transition.ref, transition.error)
        return not transition.error if transition else True

    def next_state(self, ref: Any, args: Optional[Any] = None) -> Optional[State]:
        return self._create_state(ref, args)

    def _create_state(self, ref: Any, args: Optional[Any] = None) -> Optional[Any]:
        pass

    def _save_action(self, transition: Transition):
        self._add_action(transition.action)

    def _add_action(self, action: Optional[Any]):
        pass
