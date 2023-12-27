from socialds.action.action_operator import ActionOperator


class And(ActionOperator):
    def __init__(self):
        super().__init__('and', [], [])

    def __str__(self):
        return "AND"

    def __repr__(self):
        return "AND"
