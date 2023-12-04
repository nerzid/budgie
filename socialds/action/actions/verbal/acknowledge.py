from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Acknowledge(SimpleAction):
    def __init__(self):
        self.acknowledger = DSTPronoun.I
        self.acknowledged_to = DSTPronoun.YOU
        super().__init__('acknowledge', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'
    
    def insert_pronouns(self):
        if isinstance(self.acknowledger, DSTPronoun):
            self.acknowledger = pronouns[self.acknowledger]
        if isinstance(self.acknowledged_to, DSTPronoun):
            self.acknowledged_to = pronouns[self.acknowledged_to]
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()