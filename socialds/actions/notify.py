from functools import partial

from socialds.repositories.operation_repository import create_then_add_relation, add_relation
from socialds.actions.action import Action
from socialds.actions.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.states.relation import Relation, RelationTense, RelationType


class Notify(Action):
    def __init__(self, notifier: Agent, notified_about: Relation, notified_to: Agent, negation=False):
        self.notifier = notifier
        self.notified_about = notified_about
        self.notification = Relation(notifier, RelationType.ACTION, RelationTense.FUTURE, notified_about, negation)
        super().__init__('notify', ActionObjType.FUNCTIONAL, [
            partial(add_relation, self.notification, notified_to.knowledgebase)])


# notifies other agent for an upcoming relation
# I will examine your eye now
# Joe -will do-> (Joe -examine-> Jane's eye)

# The maggot will turn into fly
# Maggot -will do-> (Maggot -turn into-> fly)
# or
# Maggot -will be-> (Maggot -is-> fly)
