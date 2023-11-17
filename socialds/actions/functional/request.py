from socialds.agent import Agent
from socialds.actions.action_obj import ActionObjType
from socialds.actions.action import Action
from socialds.states.relation import Relation


class Request(Action):
    def __init__(self, requester: Agent, requested: Relation):
        self.requester = requester
        self.requested = requested
        super().__init__('request', ActionObjType.FUNCTIONAL, [])

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.requester.name)} requests {self.requested.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}({self.requester.name} requests {self.requested}"

# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
