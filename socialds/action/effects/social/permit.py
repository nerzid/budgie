from __future__ import annotations

from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.relationstorage import RSType
from socialds.action.action import Action
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Permit(Action):
    def __init__(self, permitter: Agent | DSTPronoun, permitted: Action, permit_given_to: Agent | DSTPronoun,
                 r_tense: Tense, negation: bool):
        # self.relation = Relation(permitter, RelationType.IS_PERMITTED_TO, r_tense, permitted, negation)
        self.permitter = permitter
        self.permitted = permitted
        self.permit_given_to = permit_given_to
        self.relation = Relation(permitter, RType.IS_PERMITTED_TO, r_tense, permitted, negation)
        # super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
        #                  op_seq=[partial(add_relation, self.relation, rs)])
        super().__init__(name='permit', act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainKnowledge(knowledge=self.relation, affected=self.permit_given_to)
                         ])

    def colorless_repr(self):
        return f"{super().__repr__()}{str(self.permitter.name)} permit {self.permitted.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.permitter} permit {self.permitted}"

    def insert_pronouns(self):
        if isinstance(self.permitter, DSTPronoun):
            self.permitter = pronouns[self.permitter]
        if isinstance(self.permit_given_to, DSTPronoun):
            self.permit_given_to = pronouns[self.permit_given_to]
        self.permitted.insert_pronouns()
        self.relation.insert_pronouns()
        super().insert_pronouns()

    def execute(self):
        self.insert_pronouns()
        super().execute()
