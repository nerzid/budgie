class ExpectationStep:
    def __init__(self, action, done_by, recipient=None, unique=False):
        self.action = action
        self.unique = unique
        self.done_by = done_by
        self.recipient = recipient
