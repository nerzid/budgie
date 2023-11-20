from socialds.action.action_time import ActionTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent


class Sleep(Action):
    def __init__(self, sleeper: Agent, times: [ActionTime]=None):
        self.sleeper = sleeper
        super().__init__('sleep', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.sleeper} sleeps{super().get_times_str()}"

    def __repr__(self):
        return f"{self.sleeper} sleeps{super().get_times_str()}"
