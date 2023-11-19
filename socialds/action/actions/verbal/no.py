from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction


class No(SimpleAction):
    def __init__(self):
        super().__init__('no', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'