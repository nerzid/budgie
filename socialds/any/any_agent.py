from socialds.agent import Agent
from socialds.any.any_object import AnyObject
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor


class AnyAgent(Agent, AnyObject):
    def __init__(self):
        name = 'any-agent'
        actor = Actor('any-actor')
        roles = []
        knowledgebase = RelationStorage('')
        forgotten = RelationStorage('')
        competences = RelationStorage('')
        resources = RelationStorage('')
        places = RelationStorage('')
        super().__init__(name, actor, roles, knowledgebase, forgotten, competences, resources, places)