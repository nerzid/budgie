from typing import List

from managers.events.event import Event
from socialds.socialpractice.context.resource import Resource
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role
from socialds.managers.event_manager import EventManager


class Agent:
    def __init__(self, actor: Actor, roles: List[Role], resources: List[Resource], auto: bool = True):
        self.actor = actor
        self.roles = roles
        self.resources = resources
        self.event_manager = EventManager()
        self.auto = auto

    def act(self):
        pass

    def act_event(self, event: Event):
        pass