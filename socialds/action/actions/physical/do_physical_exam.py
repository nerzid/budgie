from __future__ import annotations

from socialds.action.action_obj import ActionObjType
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.simple_action import SimpleAction
from socialds.agent import Agent
from socialds.enums import Tense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.socialpractice.context.information import Information
from socialds.states.property import Property
from socialds.states.relation import RType


class DoPhysicalExam(SimpleAction):
    def __init__(self, exam_name: Property, exam_result_var: Property, done_by: DSTPronoun | Agent = DSTPronoun.I,
                 recipient: DSTPronoun | Agent = DSTPronoun.YOU, ):
        """
        Does a specific physical examination on patient
        Args:
            exam_name: The name of the physical exam
            exam_result_var: <leave this empty>
            done_by: The agent or DSTPronoun who does the physical exam
            recipient: The agent or DSTPronoun who has been done the physical exam on
        """
        from socialds.any.any_property import AnyProperty
        super().__init__(name='examine', done_by=done_by, recipient=recipient,
                         act_type=ActionObjType.PHYSICAL,
                         base_effects=[AddExpectedEffect(effect=GainKnowledge(knowledge=Information(
                             left=exam_result_var, rel_type=RType.IS, rel_tense=Tense.PRESENT, right=AnyProperty()
                         ), affected=done_by),
                             affected=recipient)]
                         )
        self.exam_name = exam_name
        self.exam_result_var = exam_result_var

    def __repr__(self):
        return "%s" % self.name

    @staticmethod
    def get_pretty_template():
        return "[done_by] examines [recipient] by doing [exam_name]"
