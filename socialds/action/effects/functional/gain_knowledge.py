from socialds.action.effects.effect import Effect
from socialds.conditions.agent_knows import AgentKnows
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.relationstorage import RSType
from socialds.states.any_state import AnyState
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
                             AgentKnows(agent=affected,
                                        knows=knowledge,
                                        tense=Tense.PRESENT,
                                        times=[],
                                        negation=False)
                         ],
                         affected=affected,
                         op_seq=op_seq)
