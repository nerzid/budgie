from typing import List
from functools import partial

from socialds.action.action_time import ActionTime
from socialds.enums import SemanticEvent
from socialds.action.action_obj import ActionObj, ActionObjType
from socialds.operations.operation import Operation
from socialds.operations.stateoperation import StateOperation


class Action(ActionObj):
    def __init__(self, name, act_type: ActionObjType, op_seq: List[Operation], preconditions=None,
                 times=None):
        super().__init__(name, act_type, op_seq)
        if times is None:
            times = []
        self.times = times
        if preconditions is None:
            preconditions = []
        self.name = name
        self.preconditions = preconditions

    def get_times_str(self):
        if self.times is None:
            return ''
        times_str = ''
        for time in self.times:
            times_str += str(time) + ' AND '
        if len(self.times) > 0:
            times_str = ' ' + times_str[:-5]
        return times_str

    def insert_pronouns(self):
        pass

    # def update(self, key: SemanticEvent, value: any):
    #     self.semantic_roles[key] = value
    #     return self

# doctor can examine patient's eye using ophthalmoscope
# Role -can-> Action
# Doctor -can-> Action(name="eye examination", semantic_roles)
