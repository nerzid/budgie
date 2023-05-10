from states.state import State

# e.g., Eren is tall -> name: height, value: tall
class Property(State):
    def __init__(self, name: str, value):
        super().__init__()
        self.name = name
        self.value = value