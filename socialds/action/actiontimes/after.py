from socialds.action.action import Action
from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action_time import ActionHappenedAtTime


class After(ActionHappenedAtTime):
    def __init__(self, after: Action, num_of_times: NumOfTimes = None):
        self.after = after
        self.num_of_times = num_of_times
        super().__init__()

    def __str__(self):
        if self.num_of_times is None:
            return "after %r" % self.after
        else:
            return "%s after %r" % (self.num_of_times, self.after)

    def __repr__(self):
        if self.num_of_times is None:
            return "after %r" % self.after
        else:
            return "%r after %r" % (self.num_of_times, self.after)
