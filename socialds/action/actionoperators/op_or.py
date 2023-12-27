from socialds.action.action_operator import ActionOperator


class Or(ActionOperator):
    def __init__(self):
        super().__init__('or', [], [])

    def __repr__(self):
        return "OR"
