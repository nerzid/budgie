from typing import List

from socialds.agent import Agent
from socialds.operations.stateoperation import StateOperation


class SenseVariation:
    def __init__(self, desc: str, op_seq: List[StateOperation]):
        self.desc = desc
        self.op_seq = op_seq

    def run(self):
        for op in self.op_seq:
            op.execute()


# the meaning of the action
class Sense:
    def __init__(self, desc: str, variations: List[SenseVariation]):
        """
        Meaning is used to describe what an action block does to the target object's states. Therefore, it works as a
        bridge between an action block and a sequence of state operations
        :param desc: Description of the meaning
        :param op_seq: Sequence of operations to be executed consecutively
        """
        self.desc = desc
        self.variations = variations
