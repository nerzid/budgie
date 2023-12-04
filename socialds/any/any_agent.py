from socialds.agent import Agent
from socialds.any.any_object import AnyObject
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor


class AnyAgent(Agent, AnyObject):
    def __init__(self):
        name = 'any-agent'
        actor = Actor('any-actor')
        roles = []
        super().__init__(name, actor, roles)
