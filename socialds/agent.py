from typing import List

import questionary

from socialds.relationstorage import RelationStorage
from socialds.managers.events.event import Event
from socialds.socialpractice.context.resource import Resource
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role
from socialds.managers.event_manager import EventManager
from socialds.managers.plan_manager import PlanManager
from socialds.socialpractice.activity.competence import Competence
from socialds.other.utility import merge_relation_storages


class Agent:
    def __init__(self, actor: Actor, roles: List[Role], competences: RelationStorage, auto: bool = False):
        self.actor = actor
        self.roles = roles
        self.competences = competences
        self.event_manager = EventManager()
        self.plan_manager = PlanManager()
        self.auto = auto

    def act(self):
        if self.auto:
            pass
        else:
            questionary.text(message="Choose")

    def act_event(self, event: Event):
        utt = 'Hellooooo'
        questionary.print("Other agent: " + str(utt))

    def update_competences(self):
        for role in self.roles:
            merge_relation_storages(self.competences, role.competences)
