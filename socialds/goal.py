from socialds.condition import Condition


class Goal:
    def __init__(self, conditions: [Condition]):
        self.conditions = conditions

    def is_reached(self):
        """
        Checks if the goal is reached
        :return: True if all the conditions yield true
        """
        reached = True
        for condition in self.conditions:
            reached = reached and condition.check()
        return reached
