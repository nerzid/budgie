from socialds.conditions.condition import Condition


class Goal:
    def __init__(self, owner, name: str, conditions: [Condition], desc: str = ''):
        self.name = name
        self.desc = desc
        self.conditions = conditions
        self.owner = owner

    def is_reached(self):
        """
        Checks if the goal is reached
        :return: True if all the conditions yield true
        """
        reached = True
        for condition in self.conditions:
            # print(condition)
            reached = reached and condition.check()
        return reached

    def __str__(self):
        return f'Goal: {self.name}\n' \
               f'Desc: {self.desc}\n' \
               f'Conditions: {self.conditions}'
