import uuid

from socialds.other.unique_id_generator import get_unique_id
from socialds.states.state import State


# e.g., Eren is tall -> name: height, value: tall
class Property(State):
    def __init__(self, name: str):
        super().__init__()
        self.id = get_unique_id()
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Property):
            return self.name == other.name
        else:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
        }
