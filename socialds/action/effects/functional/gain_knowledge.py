from __future__ import annotations

from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.agent_knows as an
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.information import Information
from socialds.states.relation import Negation


class GainKnowledge(Effect):

    def __init__(self, knowledge: Information, affected: 'Agent' | DSTPronoun):
        self.knowledge = knowledge
        self.affected = affected
        op_seq = [
            AddRelationToRSHolder(relation=knowledge,
                                  rsholder=affected,
                                  rstype=RSType.KNOWLEDGEBASE)
        ]
        super().__init__(name='gain-knowledge',
                         from_state=[],
                         to_state=[
                             an.AgentKnows(agent=affected,
                                           knows=knowledge,
                                           tense=Tense.PRESENT,
                                           times=[])
                         ],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'{self.affected} gain knowledge {self.knowledge}'

    @staticmethod
    def get_pretty_template():
        return "[affected] gains the knowledge [knowledge]"

    def equals_with_pronouns(self, other, pronouns):
        if not isinstance(other, GainKnowledge):
            return False
        return super().equals_with_pronouns(other, pronouns) and self.knowledge.equals_with_pronouns(other.knowledge, pronouns)

    def insert_pronouns(self):
        super().insert_pronouns()
        self.knowledge.pronouns = self.pronouns
        self.knowledge.insert_pronouns()

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.knowledge]
