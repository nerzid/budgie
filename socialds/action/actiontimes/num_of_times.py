from socialds.action.action_time import ActionTime


class NumOfTimes(ActionTime):
    def __init__(self, num: int):
        self.num = num
        super().__init__()

    def __repr__(self):
        if self.num == 1:
            times_str = 'once'
        elif self.num == 2:
            times_str = 'twice'
        elif self.num == 3:
            times_str = 'thrice'
        else:
            times_str = str(self.num)
        return f"{times_str}"
