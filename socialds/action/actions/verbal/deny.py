from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.change_property import GainKnowledge
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun


class Deny(Action):
    def __init__(self, denied):
        self.denied = denied
        from socialds.action.actions.verbal.request_confirmation import RequestConfirmation
        super().__init__('deny', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=denied, affected=DSTPronoun.YOU)
        ], preconditions=[AgentDoesAction(agent=DSTPronoun.YOU, action=RequestConfirmation(asked=denied, r_tense=Tense.ANY), tense=Tense.PAST)])

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.denied == other.denied

    def insert_pronouns(self):
        self.denied.pronouns = self.pronouns
        self.denied.insert_pronouns()
        super().insert_pronouns()
