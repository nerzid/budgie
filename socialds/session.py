from typing import List

from socialds.conditions.condition import Condition
from enum import Enum

from socialds.expectation import Expectation
from socialds.goal import Goal
from socialds.other.unique_id_generator import get_unique_id


class SessionStatus(Enum):
    NOT_STARTED = "NOT STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Session:
    def __init__(
        self,
        name: str,
        start_conditions: List[Condition],
        end_goals: List[Goal],
        expectations: List[Expectation] = None,
        status: SessionStatus = SessionStatus.NOT_STARTED,
    ):
        if expectations is None:
            expectations = []
        self.id = get_unique_id()
        self.name = name
        self.start_conditions = start_conditions
        self.expectations = expectations
        self.end_goals = end_goals
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "start_conditions": [start_condition.to_dict() for start_condition in self.start_conditions],
            "end_goals": [end_goal.to_dict() for end_goal in self.end_goals],
            "expectations": [expectation.to_dict() for expectation in self.expectations],
            "status": self.status.value,
        }

    def to_dict_with_status(self, agent):
        start_conditions_str_list = []
        expectations_str_list = []
        end_goals_str_list = []
        for start_condition in self.start_conditions:
            start_conditions_str_list.append(
                {
                    "condition": str(start_condition),
                    "status": start_condition.check(agent),
                }
            )

        for expectation in self.expectations:
            expectations_str_list.append(
                {"expectation": expectation.name, "status": expectation.status.value}
            )

        for end_goal in self.end_goals:
            end_goals_str_list.append(
                {"end_goal": end_goal.name, "status": end_goal.is_reached(agent)}
            )

        return {
            "name": self.name,
            "status": self.status.value,
            "start_conditions": start_conditions_str_list,
            "expectations": expectations_str_list,
            "end_goals": end_goals_str_list,
        }
