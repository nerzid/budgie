from __future__ import annotations

from socialds.operations.add_relation_to_agent_rs import AddRelationToAgentRS
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Notify(Action):
    def __init__(self, notifier: Agent | DSTPronoun, notified_about: Relation | Action, notified_to: Agent | DSTPronoun,
                 negation=False):
        self.notifier = notifier
        self.notified_about = notified_about
        self.notified_to = notified_to
        self.notification = Relation(notifier, RType.ACTION, Tense.FUTURE, notified_about, negation)
        super().__init__('notify', ActionObjType.FUNCTIONAL,
                         op_seq=[
                             # partial(add_relation, self.notification, notified_to.knowledgebase)
                             AddRelationToAgentRS(relation=self.notification, agent=self.notified_to,
                                                  rstype=RSType.KNOWLEDGEBASE)
                         ])

    def colorless_repr(self):
        return f"{super().__repr__()}({self.notifier.name} notify {self.notified_to} about {self.notified_about.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.notifier.name} notify {self.notified_to} about {self.notified_about})"

    def insert_pronouns(self):
        if isinstance(self.notifier, DSTPronoun):
            self.notifier = pronouns[self.notifier]
        if isinstance(self.notified_to, DSTPronoun):
            self.notified_to = pronouns[self.notified_to]
        self.notified_about.insert_pronouns()
        self.notification.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
# notifies other agent for an upcoming relation
# I will examine your eye now
# Joe -will do-> (Joe -examine-> Jane's eye)

# The maggot will turn into fly
# Maggot -will do-> (Maggot -turn into-> fly)
# or
# Maggot -will be-> (Maggot -is-> fly)
