from abc import abstractmethod
from copy import copy
from typing import List

from socialds.DSTPronounHolder import DSTPronounHolder
from socialds.conditions.SolutionStep import SolutionStep
from socialds.conditions.condition import Condition
from socialds.operations.operation import Operation
from socialds.other.dst_pronouns import DSTPronoun


class Effect(SolutionStep, DSTPronounHolder):
    def __init__(self, name: str, from_state: List[Condition], to_state: List[Condition], affected: any,
                 op_seq: List[Operation]):
        super(DSTPronounHolder, self).__init__()
        super(SolutionStep, self).__init__()
        self.op_seq = op_seq
        self.name = name
        self.from_state = from_state
        self.to_state = to_state
        self.affected = affected

    def __eq__(self, other):
        from socialds.any.any_agent import AnyAgent
        from socialds.action.action import Action

        if isinstance(other, Effect):
            if isinstance(self.affected, DSTPronoun):
                print(self.pronouns)
                affected = self.pronouns[self.affected]
            else:
                affected = self.affected

            if isinstance(other.affected, DSTPronoun):
                other_affected = self.pronouns[other.affected]
            else:
                other_affected = other.affected
            return (self.name == other.name
                    # and copied_self.op_seq == copied_other.op_seq
                    and (affected == other_affected or isinstance(affected, AnyAgent) or isinstance(other_affected, AnyAgent))
                    # and self.from_state == other.from_state
                    # and self.to_state == other.to_state
                    )
        elif isinstance(other, Action):
            if not other.specific:
                other_effects = other.base_effects + other.extra_effects
                if len(other_effects) == 1:
                    if self == other_effects[0]:
                        return True

        return False

    @abstractmethod
    def get_requirement_holders(self) -> List:
        """
        Returns instances that can have requirements.
        At the moment, it resources and places only.

        All subclasses should implement this method
        """
        return []

    def execute(self, pronouns):
        self.pronouns = pronouns
        for op in self.op_seq:
            op.pronouns = self.pronouns
            op.execute(self.pronouns)

    def insert_pronouns(self):
        if isinstance(self.affected, DSTPronoun):
            self.affected = self.pronouns[self.affected]
        for condition in self.from_state:
            print(condition)
            condition.insert_pronouns(self.pronouns)
        for condition in self.to_state:
            condition.insert_pronouns(self.pronouns)
