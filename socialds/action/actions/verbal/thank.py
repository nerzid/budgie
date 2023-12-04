from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Thank(SimpleAction):

    def __init__(self):
        self.thanker = DSTPronoun.I
        self.thanked_to = DSTPronoun.YOU
        super().__init__('thank', ActionObjType.VERBAL)

    def colorless_repr(self):
        return f'{self.thanker} {self.name} {self.thanked_to}'

    def __repr__(self):
        return f'{self.thanker} {self.name} {self.thanked_to}'

    def insert_pronouns(self):
        if isinstance(self.thanker, DSTPronoun):
            self.thanker = pronouns[self.thanker]
        if isinstance(self.thanked_to, DSTPronoun):
            self.thanked_to = pronouns[self.thanked_to]
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
