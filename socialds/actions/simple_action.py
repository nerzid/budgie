from typing import List

from socialds.operations.stateoperation import StateOperation
from socialds.actions.action import Action


class SimpleAction(Action):

    def __init__(self, name):
        super().__init__(name, op_seq=[])
