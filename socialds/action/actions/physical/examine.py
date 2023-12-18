from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Examine(SimpleAction):
    def __init__(self):
        super().__init__('examine', DSTPronoun.I, ActionObjType.PHYSICAL)

    def colorless_repr(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'
