from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action_time import ActionHappenedAtTime


class InMorning(ActionHappenedAtTime):
    def __init__(self, num_of_times: NumOfTimes = None):
        self.num_of_times = num_of_times
        super().__init__()

    def __repr__(self):
        if self.num_of_times is None:
            return f"in the morning"
        else:
            return f"{self.num_of_times} in the morning"
