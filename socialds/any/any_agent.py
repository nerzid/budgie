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
        self.id = -2

    def __eq__(self, other):
        if isinstance(other, Agent) or isinstance(other, DSTPronoun):
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
        }
