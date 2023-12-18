from enum import Enum
from typing import List

from socialds.goal import Goal


class PlanStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    FINISHED = 'FINISHED'


class Plan:
    """
    Plan is the action sequence that allows the agent to reach a certain goal (or goals)
    """
    def __init__(self, goals: List[Goal], actions):
        if actions is None:
            self.actions = []
        else:
            self.actions = actions
        self.goals = goals
        self.actions_ix = 0
        self.status = PlanStatus.NOT_STARTED

    def get_next_action(self):
        return self.actions[self.actions_ix + 1]

    def execute_next_action(self):
        if self.actions_ix <= len(self.actions) and self.status is not PlanStatus.FINISHED:
            self.status = PlanStatus.ONGOING
            self.actions[self.actions_ix].execute()
        self.actions_ix += 1
        if self.actions_ix >= len(self.actions):
            self.status = PlanStatus.FINISHED

