from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Thank(SimpleAction):

    def __init__(self):
        super().__init__('thank', DSTPronoun.I, ActionObjType.VERBAL, recipient=DSTPronoun.YOU)

    def colorless_repr(self):
        return f'{self.done_by} {self.name} {self.recipient}'

    def __repr__(self):
        return f'{self.done_by} {self.name} {self.recipient}'

    def insert_pronouns(self):
        if isinstance(self.recipient, DSTPronoun):
            self.recipient = pronouns[self.recipient]
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
