from socialds.action.action_operator import ActionOperator


class And(ActionOperator):
    def __init__(self):
        super().__init__('and', [], [])

    def colorless_repr(self):
        return f"AND"

    def __repr__(self):
        return f"AND"
