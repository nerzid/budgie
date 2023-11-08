from typing import List

import questionary

from socialds.object import Object
from socialds.relationstorage import RelationStorage
from socialds.managers.events.event import Event
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role
from socialds.managers.event_manager import EventManager
from socialds.managers.plan_manager import PlanManager
from socialds.socialpractice.activity.competence import Competence
from socialds.relationstorage import merge_relation_storages
from socialds.states.relation import Relation


class Agent(Object):
    def __init__(self, name: str, actor: Actor, roles: List[Role], competences: RelationStorage, places: RelationStorage, auto: bool = False):
        super().__init__(name)
        self.actor = actor
        self.roles = roles
        self.competences = competences
        self.places = places
        self.event_manager = EventManager()
        self.plan_manager = PlanManager()
        self.auto = auto

    def act(self):
        if self.auto:
            pass
        else:
            questionary.text(message="Choose")

    def update_competences(self):
        for role in self.roles:
            merge_relation_storages(self.competences, role.competences)
