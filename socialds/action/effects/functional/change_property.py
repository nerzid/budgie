from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.agent_knows as an
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.relation import Relation


class GainKnowledge(Effect):

    def __init__(self, knowledge: Relation, affected: any):
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
                                           times=[],
                                           negation=False)
                         ],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'{self.affected} gain knowledge {self.knowledge}'

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.knowledge == other.knowledge

    def insert_pronouns(self):
        super().insert_pronouns()
        self.knowledge.pronouns = self.pronouns
        self.knowledge.insert_pronouns()

    def get_requirement_holders(self) -> List:
        return super().get_requirement_holders() + [self.knowledge]
