from socialds.action.action_operator import ActionOperator


class Then(ActionOperator):
    def __init__(self):
        super().__init__('then', [], [])

    def __repr__(self):
        return "THEN"
