from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Listen(Action):
    def __init__(self, done_by=DSTPronoun.I, ):
        super().__init__('listen', DSTPronoun.I, ActionObjType.PHYSICAL)

    def get_requirement_holders(self) -> List:
        pass
        