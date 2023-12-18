from socialds.conditions.condition import Condition


class Goal:
    def __init__(self, name: str, conditions: [Condition], desc: str = ''):
        self.name = name
        self.desc = desc
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

    def __str__(self):
        return f'Goal: {self.name}\n' \
               f'Desc: {self.desc}\n' \
               f'Conditions: {self.conditions}'
