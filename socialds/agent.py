from socialds.socialpractice.context.resource import Resource
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role


class Agent:
    def __init__(self, actor: Actor, roles: list[Role], resources: list[Resource]):
        self.actor = actor
        self.roles = roles
        self.resources = resources
