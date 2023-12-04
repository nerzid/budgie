from __future__ import annotations

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.operations.add_relation_to_agent_rs import AddRelationToAgentRS
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class Deduce(Action):
    def __init__(self, deducer: Agent | DSTPronoun, deduced: Relation):
        """
        Agent thinks and arrives at a certain relation.
        E.g., after thinking, doctor figures out that the patient has bacterial conjunctivitis
        :param deducer: The agent who deduces the relation as fact
        :param deduced: The deduced information as relation to be stored in the deducer's knowledgebase
        """
        self.deducer = deducer
        self.deduced = deduced
        super().__init__('deduce', ActionObjType.MENTAL, op_seq=[
            AddRelationToAgentRS(relation=deduced, agent=deducer, rstype=RSType.KNOWLEDGEBASE)
        ])

    def colorless_repr(self):
        return f"{super().colorless_repr()}({self.deducer.name} deduces that {self.deduced.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.deducer.name} deduces that {self.deduced})"

    def insert_pronouns(self):
        if isinstance(self.deducer, DSTPronoun):
            self.deducer = pronouns[self.deducer]
        self.deduced.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        self.deducer.relation_storages[RSType.KNOWLEDGEBASE].add(self.deduced)
        super().execute()
