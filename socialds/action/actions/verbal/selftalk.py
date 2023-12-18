from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class SelfTalk(SimpleAction):
    def __init__(self):
        super().__init__('self-talk', DSTPronoun.I, ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.done_by} {self.name}'

    def __repr__(self):
        return f'{self.done_by} {self.name}'
    
    def insert_pronouns(self):
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()
