from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class No(SimpleAction):
    def __init__(self):
        self.noer = DSTPronoun.I
        super().__init__('no', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'
    
    def insert_pronouns(self):
        if isinstance(self.noer, DSTPronoun):
            self.noer = pronouns[self.noer]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()