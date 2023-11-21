from functools import partial

from socialds.repositories.operation_repository import create_then_add_relation, add_relation
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Notify(Action):
    def __init__(self, notifier: Agent, notified_about: Relation, notified_to: Agent, negation=False):
        self.notifier = notifier
        self.notified_about = notified_about
        self.notified_to = notified_to
        self.notification = Relation(notifier, RType.ACTION, Tense.FUTURE, notified_about, negation)
        super().__init__('notify', ActionObjType.FUNCTIONAL, [
            partial(add_relation, self.notification, notified_to.knowledgebase)])

    def colorless_repr(self):
        return f"{super().__repr__()}({self.notifier.name} notifies {self.notified_to} about {self.notified_about.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.notifier.name} notifies {self.notified_to} about {self.notified_about})"
# notifies other agent for an upcoming relation
# I will examine your eye now
# Joe -will do-> (Joe -examine-> Jane's eye)

# The maggot will turn into fly
# Maggot -will do-> (Maggot -turn into-> fly)
# or
# Maggot -will be-> (Maggot -is-> fly)
