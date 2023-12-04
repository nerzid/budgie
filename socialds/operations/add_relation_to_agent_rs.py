from __future__ import annotations

from socialds.agent import Agent
from socialds.operations.add_relation import AddRelation
from socialds.operations.stateoperation import StateOperation
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.states.relation import Relation
from socialds.other.dst_pronouns import pronouns


class AddRelationToAgentRS(StateOperation):
    def __init__(self, relation: Relation | StateOperation, agent: Agent | DSTPronoun | StateOperation,
                 rstype: RSType):
        super().__init__('add-relation-to-agent-rs')
        self.relation = relation
        self.agent = agent
        self.rstype = rstype

    def execute_param_state_operations(self):
        if isinstance(self.relation, StateOperation):
            self.relation = self.relation.execute()
        elif isinstance(self.agent, StateOperation):
            self.agent = self.agent.execute()
        elif isinstance(self.agent, DSTPronoun):
            self.agent = pronouns[self.agent]

    def execute(self):
        self.execute_param_state_operations()
        self.relation.insert_pronouns()
        self.agent.relation_storages[self.rstype].add(self.relation)
