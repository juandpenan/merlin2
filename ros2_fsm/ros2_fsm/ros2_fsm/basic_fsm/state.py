

from typing import List
from abc import ABC, abstractmethod
from .blackboard import Blackboard


class State(ABC):

    def __init__(self, outcomes: List[str]):
        self._outcomes = []
        self._canceled = False

        if outcomes:
            self._outcomes = outcomes
        else:
            raise Exception("There mmust be at least one outcome")

    def __call__(self, blackboard: Blackboard):
        self._canceled = False
        return self.execute(blackboard)

    @abstractmethod
    def execute(self, blackboard: Blackboard) -> str:
        """ state execution """

    def __str__(self):
        return self.__class__.__name__

    def restart_canceled(self):
        self._canceled = False

    def cancel_state(self):
        self._canceled = True

    def is_canceled(self):
        return self._canceled

    def get_outcomes(self) -> List[str]:
        return self._outcomes
