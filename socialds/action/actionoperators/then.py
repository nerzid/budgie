from socialds.action.action_operator import ActionOperator


class Then(ActionOperator):
    def __init__(self):
        super().__init__('then', [])

    def colorless_repr(self):
        return f"THEN"

    def __repr__(self):
        return f"THEN"
