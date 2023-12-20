from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Greet(SimpleAction):
    def __init__(self):
        super().__init__('greet', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, recipient=DSTPronoun.YOU)

    def colorless_repr(self):
        return f'{self.done_by} {self.name} {self.recipient}'

    def __repr__(self):
        return f'{self.done_by} {self.name} {self.recipient}'
