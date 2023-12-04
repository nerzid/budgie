from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Backchannel(SimpleAction):
    def __init__(self):
        self.backchanneler = DSTPronoun.I
        super().__init__('backchannel', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.backchanneler} {self.name}'

    def __repr__(self):
        return f'{self.backchanneler} {self.name}'
    
    def insert_pronouns(self):
        if isinstance(self.backchanneler, DSTPronoun):
            self.backchanneler = pronouns[self.backchanneler]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()