from socialds.action.actiontimes.num_of_times import NumOfTimes
from socialds.action.action import Action
from socialds.action.action_time import ActionTime


class Before(ActionTime):
    def __init__(self, before: Action, num_of_times: NumOfTimes = None):
        self.num_of_times = num_of_times
        self.before = before
        super().__init__()

    def __str__(self):
        if self.num_of_times is None:
            return "before %s" % self.before
        else:
            return "%s before %s" % (self.num_of_times, self.before)

    def __repr__(self):
        if self.num_of_times is None:
            return "before %r" % self.before
        else:
            return "%s before %r" % (self.num_of_times, self.before)
