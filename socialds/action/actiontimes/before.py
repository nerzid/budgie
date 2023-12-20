from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action import Action
from socialds.action.action_time import ActionTime


class Before(ActionTime):
    def __init__(self, before: Action, num_of_times: NumOfTimes = None):
        self.num_of_times = num_of_times
        self.before = before
        super().__init__()

    def colorless_repr(self):
        if self.num_of_times is None:
            return f"before {self.before.colorless_repr()}"
        else:
            return f"{self.num_of_times} before {self.before.colorless_repr()}"

    def __repr__(self):
        if self.num_of_times is None:
            return f"before {self.before}"
        else:
            return f"{self.num_of_times} before {self.before}"

    def insert_pronouns(self):
        self.before.insert_pronouns()
        super().insert_pronouns()
