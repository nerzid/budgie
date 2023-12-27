from socialds.action.action import Action
from socialds.action.action_operator import ActionOperator
from socialds.conditions.condition import Condition


class When(ActionOperator):
    def __init__(self, action: Action, conditions: [Condition]):
        self.action = action
        self.conditions = conditions
        super().__init__('when', [], [])

    def __str__(self):
        conditions_str = ""
        for condition in self.conditions:
            conditions_str += "%r\n" % condition
        conditions_str = conditions_str[:-1]
        return "WHEN %s DO %r" % (conditions_str, self.action)

    def __repr__(self):
        conditions_str = ""
        for condition in self.conditions:
            conditions_str += "%r\n" % condition
        conditions_str = conditions_str[:-1]
        return "WHEN %s DO %r" % (conditions_str, self.action)

    def insert_pronouns(self):
        self.action.insert_pronouns()
        for condition in self.conditions:
            condition.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
