from typing import List

from socialds.conditions.SolutionStep import SolutionStep
from socialds.conditions.condition import Condition
from socialds.enums import Priority


class ConditionSolution:
    def __init__(
        self,
        condition: Condition,
        steps: List[SolutionStep] = None,
        name: str = "",
        desc: str = "",
        priority: Priority = Priority.MID,
    ):
        """
        This class holds actions to execute in order to satisfy the given condition
        @param condition:
        @param steps:
        """
        self.name = name
        self.desc = desc
        if steps is None:
            steps = []
        self.condition = condition
        self.steps = steps
        self.priority = priority

    def __repr__(self):
        text = f"Condition: {self.condition} can be solved {self.desc}\n"
        i = 1
        for step in self.steps:
            text += f"Step {str(i)}: {step}"
            i += 1
        return text

    def add_steps(self, step: SolutionStep):
        self.steps.append(step)
