from socialds.agent import Agent
from socialds.actions.action_obj import ActionObjType
from socialds.actions.action import Action
from socialds.states.relation import Relation


class Request(Action):
    def __init__(self, requester: Agent, requested_relation: Relation):
        self.requester = requester
        self.requested_relation = requested_relation
        super().__init__('request', ActionObjType.FUNCTIONAL, [])

# Can Joe come into the office?
# request to enter the place
# it is a request for the following Joe -move-> office assuming
# requester -> relation
