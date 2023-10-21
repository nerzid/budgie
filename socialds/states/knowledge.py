from socialds.states.state import State


class Knowledge(State):
    def __init__(self, value):
        super().__init__()
        self.value = value
