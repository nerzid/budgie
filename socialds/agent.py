from typing import List, Optional, Dict

import questionary

from socialds.managers.event_manager import EventManager
from socialds.managers.planner import Planner
from socialds.object import Object
from socialds.relationstorage import RelationStorage, RSType
from socialds.relationstorage import merge_relation_storages
from socialds.rs_holder import RSHolder, RSHolderType
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role


class Agent(Object, RSHolder):
    def __init__(self, name: str, actor: Actor, roles: List[Role], relation_storages: Dict[RSType, RelationStorage] = None, auto: bool = False):
        Object.__init__(self, name=name)
        RSHolder.__init__(self, rsholder_name=name,
                          rsholder_type=RSHolderType.AGENT,
                          relation_storages=relation_storages)

        self.actor = actor
        self.roles = roles
        self.planner = Planner(self)
        self.auto = auto

        self.update_competences_from_roles()
        # adds the knowledgebase into the agent's knowledgebase
        merge_relation_storages(self.relation_storages[RSType.KNOWLEDGEBASE], actor.knowledgebase)

    def __repr__(self):
        return f'{self.name}'

    def act(self):
        if self.auto:
            pass
        else:
            pass
        self.planner.plan()

    def update_competences_from_roles(self):
        for role in self.roles:
            merge_relation_storages(self.relation_storages[RSType.COMPETENCES], role.competences)

    def info(self):
        pretty_info = ''
        pretty_info += self.name + ' auto=' + str(self.auto) + '\n'
        pretty_info += str(self.relation_storages[RSType.KNOWLEDGEBASE]) + '\n'
        pretty_info += str(self.relation_storages[RSType.COMPETENCES]) + '\n'
        # pretty_info += str(self.actor.knowledgebase) + '\n'
        for role in self.roles:
            pretty_info += role.name + '\n' + role.competences + '\n'
        # # pretty_info += str(self.roles) + '\n'
        # pretty_info += str(self.competences) + '\n'
        # pretty_info += str(self.resources) + '\n'
        pretty_info += str(self.relation_storages[RSType.PLACES])
        return pretty_info
