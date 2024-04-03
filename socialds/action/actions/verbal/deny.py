from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.change_property import GainKnowledge
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
import socialds.action.actions.verbal.request_confirmation as rc
from socialds.states.relation import Relation, RType


class Deny(Action):
    def __init__(self, denied):
        self.denied = denied
        super().__init__('deny', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, base_effects=[
            GainKnowledge(knowledge=denied, affected=DSTPronoun.YOU)
        ])

    def equals_with_pronouns(self, other, pronouns):
        return super().equals_with_pronouns(other, pronouns) and self.denied == other.denied

    def check_preconditions(self, checker):
        return super().check_preconditions(checker) and \
            AgentDoesAction(agent=DSTPronoun.YOU, action=Relation(left=DSTPronoun.YOU, rtype=RType.ACTION,
                                                                  rtense=Tense.PAST,
                                                                  right=rc.RequestConfirmation(done_by=DSTPronoun.YOU,
                                                                                               asked=self.denied,
                                                                                               r_tense=Tense.ANY,
                                                                                               recipient=DSTPronoun.I)),
                            tense=Tense.PAST).check(checker=checker)

    def insert_pronouns(self):
        self.denied.pronouns = self.pronouns
        self.denied.insert_pronouns()
        super().insert_pronouns()
