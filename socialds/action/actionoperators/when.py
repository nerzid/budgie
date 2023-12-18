from socialds.action.action import Action
from socialds.action.action_operator import ActionOperator
from socialds.conditions.condition import Condition


class When(ActionOperator):
    def __init__(self, action: Action, conditions: [Condition]):
        self.action = action
        self.conditions = conditions
        super().__init__('when', [], [])

    def colorless_repr(self):
        conditions_str = ""
        for condition in self.conditions:
            conditions_str += condition.colorless_repr() + '\n'
        conditions_str = conditions_str[:-1]
        return f"{super().colorless_repr()}WHEN {conditions_str} DO {self.action.colorless_repr()}"

    def __repr__(self):
        conditions_str = ""
        for condition in self.conditions:
            conditions_str += str(condition) + '\n'
        conditions_str = conditions_str[:-1]
        return f"{super().__repr__()}WHEN {conditions_str} DO {self.action.colorless_repr()}"

    def insert_pronouns(self):
        self.action.insert_pronouns()
        for condition in self.conditions:
            condition.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
