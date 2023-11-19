from typing import List

from socialds.operations.stateoperation import StateOperation
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType


class SimpleAction(Action):

    def __init__(self, name: str, act_type: ActionObjType):
        super().__init__(name, act_type, [])
