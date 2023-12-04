from typing import List, Optional

import questionary

from socialds.managers.event_manager import EventManager
from socialds.managers.plan_manager import PlanManager
from socialds.object import Object
from socialds.relationstorage import RelationStorage, RSType
from socialds.relationstorage import merge_relation_storages
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role


class Agent(Object):
    def __init__(self, name: str, actor: Actor, roles: List[Role], relation_storages: dict = None, auto: bool = False):
        super().__init__(name)

        self.actor = actor
        if relation_storages is None:
            self.relation_storages = {
                RSType.KNOWLEDGEBASE: RelationStorage(actor.name + ' Knowledgebase'),
                RSType.FORGOTTEN: RelationStorage(actor.name + ' Forgotten'),
                RSType.COMPETENCES: RelationStorage(actor.name + ' Competences'),
                RSType.RESOURCES: RelationStorage(actor.name + ' Resources'),
                RSType.PLACES: RelationStorage(actor.name + ' Places')
            }
        else:
            self.relation_storages = relation_storages
        self.roles = roles
        self.plan_manager = PlanManager()
        self.auto = auto

        # adds the knowledgebase into the agent's knowledgebase
        merge_relation_storages(self.relation_storages[RSType.KNOWLEDGEBASE], actor.knowledgebase)

    def __repr__(self):
        return f'{self.name}'

    def act(self):
        if self.auto:
            pass
        else:
            pass
        self.plan_manager.plan()

    def update_competences(self):
        for role in self.roles:
            merge_relation_storages(self.relation_storages[RSType.COMPETENCES], role.competences)

    def info(self):
        pretty_info = ''
        pretty_info += self.name + ' auto=' + str(self.auto) + '\n'
        pretty_info += str(self.relation_storages[RSType.KNOWLEDGEBASE]) + '\n'
        # pretty_info += str(self.actor.knowledgebase) + '\n'
        for role in self.roles:
            pretty_info += role.name + '\n' + role.competences + '\n'
        # # pretty_info += str(self.roles) + '\n'
        # pretty_info += str(self.competences) + '\n'
        # pretty_info += str(self.resources) + '\n'
        pretty_info += str(self.relation_storages[RSType.PLACES])
        return pretty_info
