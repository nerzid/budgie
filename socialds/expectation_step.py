class ExpectationStep:
    def __init__(
        self, action, action_attrs: dict, done_by, recipient=None, unique=False
    ):
        self.action = action
        self.action_attrs = action_attrs
        self.unique = unique
        self.done_by = done_by
        self.recipient = recipient
