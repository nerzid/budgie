from socialds.action.action_time import ActionTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.states.property import Property


class Have(Action):
    def __init__(self, owner: Agent, target: Property, times: [ActionTime] = None):
        self.owner = owner
        self.target = target
        super().__init__('has', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.owner} has {self.target}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.owner} has {self.target}{super().get_times_str()}"
