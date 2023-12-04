from __future__ import annotations

from functools import partial

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.operations.add_relation_to_agent_rs import AddRelationToAgentRS
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class Learn(Action):

    def __init__(self, learner: Agent | DSTPronoun, learned: Relation):
        """
        Learns a piece of information as relation. Learn is similar to Share except only agent who does
        the action saves the new information in their knowledgebase.
        :param learner: The agent who learns the new information
        :param learned: Information to be learned and saved in agent's knowledgebase e.g., patient's eye -has-> inflammation
        """
        self.learner = learner
        self.learned = learned
        super().__init__(name="learn", act_type=ActionObjType.FUNCTIONAL,
                         # op_seq=[partial(add_relation, learned, learner.knowledgebase)]
                         op_seq=[
                             AddRelationToAgentRS(relation=learned, agent=self.learner, rstype=RSType.KNOWLEDGEBASE)
                         ]
                         )

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.learner} learns {self.learned.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.learner} learns {self.learned}"

    def insert_pronouns(self):
        if isinstance(self.learner, DSTPronoun):
            self.learner = pronouns[self.learner]
        self.learned.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
