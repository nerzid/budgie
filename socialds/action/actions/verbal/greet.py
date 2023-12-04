from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class Greet(SimpleAction):
    def __init__(self):
        super().__init__('greet', ActionObjType.VERBAL)
        self.greeter = DSTPronoun.I
        self.greeted_to = DSTPronoun.YOU

    def colorless_repr(self):
        return f'{self.greeter} {self.name} {self.greeted_to}'

    def __repr__(self):
        return f'{self.greeter} {self.name} {self.greeted_to}'

    def insert_pronouns(self):
        if isinstance(self.greeter, DSTPronoun):
            self.greeter = pronouns[self.greeter]
        if isinstance(self.greeted_to, DSTPronoun):
            self.greeted_to = pronouns[self.greeted_to]

    def execute(self):
        self.insert_pronouns()
        super().execute()
