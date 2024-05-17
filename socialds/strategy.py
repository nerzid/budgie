from typing import List
from socialds.action.action import Action
from socialds.conditions.condition import Condition
from socialds.enums import Priority
from socialds.goal import Goal


class Strategy:
    def __init__(
        self, conditions: List[Condition], actions: List[Action], done_by
    ) -> None:
        self.conditions = conditions
        self.actions = actions
        self.done_by = done_by

    def check(self):
        result = True
        for condition in self.conditions:
            result = result and condition.check(self.done_by)
        return result

    def create_high_priority_goal(self):
        return Goal(
            owner=self.done_by,
            name="strategy",
            conditions=self.conditions,
            known_by=self.done_by,
            priority=Priority.HIGH,
        )
