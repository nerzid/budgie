from socialds.action.action_time import ActionHappenedAtTime


class InDay(ActionHappenedAtTime):
    def __init__(self, num):
        self.num = num
        super().__init__()

    def __repr__(self):
        return f"in {self.num} day"
