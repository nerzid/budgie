from socialds.states.state import State


# e.g., Eren is tall -> name: height, value: tall
class Property(State):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __repr__(self):
        return self.name
