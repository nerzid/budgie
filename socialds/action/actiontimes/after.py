from socialds.action.action import Action
from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action_time import ActionTime


class After(ActionTime):
    def __init__(self, after: Action, num_of_times: NumOfTimes = None):
        self.after = after
        self.num_of_times = num_of_times
        super().__init__()

    def colorless_repr(self):
        if self.num_of_times is None:
            return f"after {self.after.colorless_repr()}"
        else:
            return f"{self.num_of_times} after {self.after.colorless_repr()}"

    def __repr__(self):
        if self.num_of_times is None:
            return f"after {self.after}"
        else:
            return f"{self.num_of_times} after {self.after}"
