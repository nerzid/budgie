from typing import List

import questionary

from socialds.managers.event_manager import EventManager
from socialds.managers.plan_manager import PlanManager
from socialds.object import Object
from socialds.relationstorage import RelationStorage
from socialds.relationstorage import merge_relation_storages
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role


class Agent(Object):
    def __init__(self, name: str, actor: Actor, roles: List[Role], knowledgebase: RelationStorage,
                 competences: RelationStorage, resources: RelationStorage, places: RelationStorage, auto: bool = False):
        super().__init__(name)
        self.actor = actor
        self.roles = roles
        self.knowledgebase = knowledgebase
        self.competences = competences
        self.resources = resources
        self.places = places
        self.plan_manager = PlanManager()
        self.auto = auto

        # adds the knowledgebase into the agent's knowledgebase
        merge_relation_storages(self.knowledgebase, actor.knowledgebase)

    def act(self):
        if self.auto:
            pass
        else:
            pass
        self.plan_manager.plan()

    def update_competences(self):
        for role in self.roles:
            merge_relation_storages(self.competences, role.competences)

    def info(self):
        pretty_info = ''
        pretty_info += self.name + ' auto=' + str(self.auto) + '\n'
        pretty_info += str(self.knowledgebase) + '\n'
        # pretty_info += str(self.actor.knowledgebase) + '\n'
        for role in self.roles:
            pretty_info += role.name + '\n' + role.competences + '\n'
        # # pretty_info += str(self.roles) + '\n'
        # pretty_info += str(self.competences) + '\n'
        # pretty_info += str(self.resources) + '\n'
        pretty_info += str(self.places)
        return pretty_info
