from __future__ import annotations

from typing import List

from socialds.action.action_obj import ActionObjType
from socialds.action.effects.effect import Effect
from socialds.action.effects.social.gain_permit import GainPermit
from socialds.agent import Agent
from socialds.conditions.has_permit import HasPermit
from socialds.other.dst_pronouns import DSTPronoun
from socialds.action.action import Action
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Permit(Action):
    def __init__(self, done_by: Agent | DSTPronoun, permitted: Action | Effect, permit_given_to: Agent | DSTPronoun,
                 r_tense: Tense, negation: bool):
        # self.relation = Relation(permitter, RelationType.IS_PERMITTED_TO, r_tense, permitted, negation)
        self.permitted = permitted
        self.permit_given_to = permit_given_to
        self.relation = Relation(permit_given_to, RType.IS_PERMITTED_TO, r_tense, permitted, negation)
        # super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
        #                  op_seq=[partial(add_relation, self.relation, rs)])
        super().__init__(name='permit',
                         done_by=done_by,
                         act_type=ActionObjType.VERBAL,
                         base_effects=[
                             GainPermit(permit=self.relation, affected=self.permit_given_to)
                         ])

    def __str__(self):
        return f"{self.done_by} gives permit for {self.permitted}"

    def __repr__(self):
        return f"{str(self.done_by.name)} gives permit for {self.permitted}"

    @staticmethod
    def get_pretty_template():
        return "[done_by] gives permit for [permitted] to [permit_given_to] ([r_tense][negation])"

    def get_requirement_holders(self) -> List:
        return [self.done_by, self.permit_given_to]

    def insert_pronouns(self):
        if isinstance(self.permit_given_to, DSTPronoun):
            self.permit_given_to = self.pronouns[self.permit_given_to]
        self.permitted.pronouns = self.pronouns
        self.relation.pronouns = self.pronouns
        self.permitted.insert_pronouns()
        self.relation.insert_pronouns()
        super().insert_pronouns()

    def check_preconditions(self, checker):
        return super().check_preconditions(checker=checker) and \
            HasPermit(agent=self.done_by, permit=self.permitted).check(checker=checker)
