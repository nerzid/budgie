import textwrap
from enum import Enum
from typing import List

from socialds.action.action_obj import ActionObj
from socialds.action.effects.effect import Effect
from socialds.conditions.condition import Condition
from socialds.expectation import Expectation, ExpectationType, ExpectationStatus


class NormStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    FOLLOWED = 'FOLLOWED'
    VIOLATED = 'VIOLATED'
    SKIPPED = 'SKIPPED'
    COMPLETED = 'COMPLETED'


class Norm(Expectation):
    def __init__(self, name: str,
                 action_seq: List[ActionObj],
                 violation_conditions: List[Condition] = None,
                 skipping_conditions: List[Condition] = None,
                 violation_effects: List[Effect] = None,
                 skipping_effects: List[Effect] = None,
                 completion_effects: List[Effect] = None):
        super().__init__(name, ExpectationType.NORM, ExpectationStatus.NOT_STARTED, action_seq)
        if violation_conditions is None:
            violation_conditions = []
        if skipping_conditions is None:
            skipping_conditions = []
        if violation_effects is None:
            violation_effects = []
        if skipping_effects is None:
            skipping_effects = []
        if completion_effects is None:
            completion_effects = []
        self.norm_status = NormStatus.NOT_STARTED
        self.violation_conditions = violation_conditions
        self.skipping_conditions = skipping_conditions
        self.violation_effects = violation_effects
        self.skipping_effects = skipping_effects
        self.completion_effects = completion_effects

    def __repr__(self):
        text = 'Norm: ' + self.name + '(' + self.status.value + ')' + '\n'

        text += 'Actions:\n'
        i = 1
        for action in self.action_seq:
            text += textwrap.indent(text="%i-) %s\n" % (i, action), prefix='  ')
            i += 1

        text += 'Skipping Conditions \n'
        for condition in self.skipping_conditions:
            text += textwrap.indent(text="%s\n" % condition, prefix='  ')

        text += 'Completion Effects \n'
        for effect in self.completion_effects:
            text += textwrap.indent(text="%s\n" % effect, prefix='  ')

        text += 'Violation Effects \n'
        for effect in self.violation_effects:
            text += textwrap.indent(text="%s\n" % effect, prefix='  ')
        return text

    def update_status(self, agent):

        """
        The expectation status of a norm can be not_started, ongoing, completed or failed.
        Every norm starts as not_started by default. Then after the dialogue system is initialized
        their statuses are updated based on the variables in the dialogue system. This means that some of
        the expectations' status might be updated to something else than not_started if the certain conditions
        are fulfilled.
        Therefore, this method checks if these certain conditions are fulfilled,
        and updates the status of the expectation to a new value

        Criteria for the status update:
        Every expectation starts with the status NOT_STARTED by default
        if the actions in the action seq can be found in the dialogue history,
        then the status is COMPLETED

        if the actions in the action seq cannot be found in the dialogue history,
        AND the start_conditions are TRUE
        AND the end_conditions are FALSE
        then the status is ONGOING

        if the actions in the action seq cannot be found in the dialogue history,
        AND the start_conditions are TRUE
        AND the end_conditions are TRUE
        then the status is FAILED.
        (This might need to change. Usually we reconsinder if we need to perform the actual action or
         reaching certain conditions is sufficient)

        if the actions in the act

        """
        super().update_status(agent)
        if self.status == ExpectationStatus.COMPLETED or self.status == ExpectationStatus.FAILED:
            return

        self.update_norm_status(agent)

    def update_norm_status(self, agent):
        """
        Updates the norm status alongside its expectation status. The norm status can be as followed:

        Every norm starts with NOT_STARTED norm_status by default
        if any skipping conditions are true then the norm is SKIPPED
        if any violation conditions are true then the norm is VIOLATED
        if all the start conditions are true and the norm status is not SKIPPED or VIOLATED,
        then it is FOLLOWED
        """
        if self.norm_status == NormStatus.SKIPPED or self.norm_status == NormStatus.VIOLATED:
            return

        a_condition_is_true = False
        for condition in self.skipping_conditions:
            print(condition)
            if condition.check(agent) is False:
                a_condition_is_true = True
                break
        if a_condition_is_true:
            self.norm_status = NormStatus.SKIPPED
            self.status = ExpectationStatus.COMPLETED
            self.activate_effects(self.skipping_effects)
            return

        a_condition_is_true = False
        for condition in self.violation_conditions:
            if condition.check(agent) is False:
                a_condition_is_true = True
                break
        if a_condition_is_true:
            self.norm_status = NormStatus.VIOLATED
            self.status = ExpectationStatus.FAILED
            self.activate_effects(self.violation_effects)
            return

        if self.status == ExpectationStatus.ONGOING:
            self.norm_status = NormStatus.FOLLOWED
        elif self.status == ExpectationStatus.COMPLETED:
            self.norm_status = NormStatus.COMPLETED

    def activate_effects(self, effects: List[Effect]):
        for effect in effects:
            effect.execute()
