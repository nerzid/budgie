from copy import copy
from typing import List

from socialds.conditions.SolutionStep import SolutionStep
from socialds.conditions.condition import Condition
from socialds.operations.operation import Operation
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Effect(SolutionStep):
    def __init__(self, name: str, from_state: List[Condition], to_state: List[Condition], affected: any,
                 op_seq: List[Operation]):
        self.op_seq = op_seq
        self.name = name
        self.from_state = from_state
        self.to_state = to_state
        self.affected = affected

    def __eq__(self, other):
        from socialds.any.any_agent import AnyAgent
        if isinstance(other, Effect):
            # copied_self = copy(self)
            # copied_self.insert_pronouns()
            #
            # copied_other = copy(other)
            # copied_other.insert_pronouns()
            return (self.name == other.name
                    # and copied_self.op_seq == copied_other.op_seq
                    and (self.affected == other.affected or isinstance(self.affected, AnyAgent) or isinstance(other.affected, AnyAgent))
                    and self.from_state == other.from_state
                    and self.to_state == other.to_state)
        return False

    def execute(self):
        for op in self.op_seq:
            op.execute()

    def insert_pronouns(self):
        if isinstance(self.affected, DSTPronoun):
            self.affected = pronouns[self.affected]
        for condition in self.from_state:
            condition.insert_pronouns()
        for condition in self.to_state:
            condition.insert_pronouns()
