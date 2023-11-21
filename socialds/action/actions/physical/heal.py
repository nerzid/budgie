from typing import List

from socialds.action.action_time import ActionTime
from socialds.action.action_obj import ActionObjType
from socialds.action.action import Action
from socialds.states.property import Property


class Heal(Action):
    def __init__(self, healed: Property, healer: any = None, negation: bool = False, times: List[ActionTime] = None):
        self.healed = healed
        self.healer = healer
        self.negation = negation
        super().__init__('heal', ActionObjType.PHYSICAL, [], times=times)

    def colorless_repr(self):
        if self.healer is None:
            negation_str = (f"is healed", f"isn't healed")[self.negation]
            return f"{self.healed} {negation_str}{super().get_times_str()}"
        else:
            negation_str = (f"heals", f"doesn't heal")[self.negation]
            return f"{self.healer} {negation_str} {self.healed}{super().get_times_str()}"

    def __repr__(self):
        if self.healer is None:
            negation_str = (f"is healed", f"isn't healed")[self.negation]
            return f"{self.healed} {negation_str}{super().get_times_str()}"
        else:
            negation_str = (f"heals", f"doesn't heal")[self.negation]
            return f"{self.healer} {negation_str} {self.healed}{super().get_times_str()}"
