from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class SelfTalk(SimpleAction):
    def __init__(self):
        self.selftaker = DSTPronoun.I
        super().__init__('self-talk', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.selftaker} {self.name}'

    def __repr__(self):
        return f'{self.selftaker} {self.name}'
    
    def insert_pronouns(self):
        if isinstance(self.selftalker, DSTPronoun):
            self.selftaker = pronouns[self.selftaker]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()