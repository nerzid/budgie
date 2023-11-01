from object import Object
from states.state import State


# e.g., Eren likes apples -> left: Eren, name: likes, right: apples
class Relation(State):
    def __init__(self, left: Object, name: str, right: Object):
        super().__init__()
        self.left = left
        self.name = name
        self.right = right

    def __str__(self):
        return str(self.left) + " ---" + self.name + "---> " + str(self.right)
