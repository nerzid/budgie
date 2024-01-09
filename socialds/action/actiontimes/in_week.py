from socialds.action.action_time import ActionHappenedAtTime


class InWeek(ActionHappenedAtTime):
    def __init__(self, num: int):
        super().__init__()
        self.num = num

    def __repr__(self):
        return f"in {self.num} week"
