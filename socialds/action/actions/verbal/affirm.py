from typing import List

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun


class Affirm(Action):

    def __init__(self, affirmed):
        self.affirmed = affirmed
        from socialds.action.actions.verbal.request_confirmation import RequestConfirmation
        super().__init__('affirm', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=affirmed, affected=DSTPronoun.YOU)
        ], preconditions=[AgentDoesAction(agent=DSTPronoun.YOU, action=RequestConfirmation(asked=affirmed, r_tense=Tense.ANY), tense=Tense.PAST)])

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.affirmed == other.affirmed

    def insert_pronouns(self):
        self.affirmed.pronouns = self.pronouns
        self.affirmed.insert_pronouns()
        super().insert_pronouns()
