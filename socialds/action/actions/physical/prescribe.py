from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.action_time import ActionTime
from socialds.agent import Agent
from socialds.states.property import Property


class Prescribe(Action):

    def __init__(self, prescriber: Agent, prescribed: [Property], prescribed_for: Agent, negation: bool = False,
                 times=None):
        self.prescriber = prescriber
        self.prescribed = prescribed
        self.prescribed_for = prescribed_for
        self.negation = negation
        self.times = times
        super().__init__('prescribe', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        return f"{self.prescriber} prescribes {self.prescribed} for {self.prescribed_for}{super().get_times_str()}"

    def __repr__(self):
        return f"{self.prescriber} prescribes {self.prescribed} for {self.prescribed_for}{super().get_times_str()}"
