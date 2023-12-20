from socialds.agent import Agent
from socialds.any.any_object import AnyObject
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor


class AnyAgent(Agent, AnyObject):
    def __init__(self):
        name = 'any-agent'
        actor = Actor('any-actor')
        roles = []
        super().__init__(name, actor, roles)

    def __eq__(self, other):
        if isinstance(other, Agent) or isinstance(other, DSTPronoun):
            return True
        return False
