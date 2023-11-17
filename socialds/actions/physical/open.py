from socialds.agent import Agent
from socialds.actions.action_obj import ActionObjType
from socialds.actions.simple_action import SimpleAction


class Open(SimpleAction):
    def __init__(self, target: any, by: Agent):
        self.target = target
        self.by = by
        super().__init__('open', ActionObjType.PHYSICAL)

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.by.name)} opens {self.target.name}"

    def __repr__(self):
        return f"{super().__repr__()}({self.by.name} opens {self.target.name}"
