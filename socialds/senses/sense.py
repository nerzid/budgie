from typing import List

from socialds.actions.action import ActionObj
from socialds.agent import Agent
from socialds.operations.stateoperation import StateOperation


class SenseVariation:
    def __init__(self, desc: str, action_seq: List[ActionObj]):
        self.desc = desc
        self.action_seq = action_seq


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
