from copy import copy
from enum import Enum
from typing import List

from socialds.action.action_obj import ActionObj
from socialds.enums import Tense, DSAction, DSActionByType
from socialds.expectation_step import ExpectationStep
from socialds.message import Message


class ExpectationType(Enum):
    NORM = 'norm'
    STRATEGY = 'strategy'


class ExpectationStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class Expectation:
    def __init__(self, name: str, etype: ExpectationType, status: ExpectationStatus, steps: List[ExpectationStep],
                 repeatable=False):
        """
        Creates an expectation of an action sequence that is expected to be seen during the dialogue.
        For example, norms are type of expectations that are expected to be performed by the agents
        There are various norms such as cultural norms, social norms, etc.
        @param name:
        @param etype:
        @param status:
        @param steps:
        """
        self.repeatable = repeatable
        self.name = name
        self.etype = etype
        self.status = status
        self.step = steps
        self.steps_left = copy(steps)
        self.steps_done = []

    def update_status(self, agent):
        steps_to_be_removed = []
        for step in self.steps_left:
            from socialds.action.action import Action
            action = step.action
            if isinstance(action, Action):
                from socialds.states.relation import Relation
                from socialds.states.relation import RType

                # from socialds.any.any_agent import AnyAgent
                if agent.dialogue_system.last_turn_actions.contains(
                        Relation(left=agent,
                                 rtense=Tense.ANY,
                                 rtype=RType.ACTION,
                                 right=action),
                        agent.pronouns):
                    is_to_be_removed = False
                    for step_to_be_removed in steps_to_be_removed:
                        if action.equals_with_pronouns(step_to_be_removed.action, agent.pronouns):
                            is_to_be_removed = True
                    if not is_to_be_removed:
                        steps_to_be_removed.append(step)
                        self.status = ExpectationStatus.ONGOING
                        continue
        for step in steps_to_be_removed:
            self.steps_left.remove(step)
            self.steps_done.append(step)
        if len(self.steps_left) == 0:
            if self.status is not ExpectationStatus.COMPLETED:
                self.status = ExpectationStatus.COMPLETED
                agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                   ds_action_by='Dialogue System',
                                                   message='Expectation {} is completed!'.format(self.name),
                                                   ds_action=DSAction.DISPLAY_LOG.value))
                if self.repeatable:
                    self.status = ExpectationStatus.NOT_STARTED
                    agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                       ds_action_by='Dialogue System',
                                                       message='Expectation {} can be repeated again now!'.format(self.name),
                                                       ds_action=DSAction.DISPLAY_LOG.value))
            elif self.status is ExpectationStatus.COMPLETED:
                pass
            else:
                self.status = ExpectationStatus.FAILED
                agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                   ds_action_by='Dialogue System',
                                                   message='Expectation {} is failed!'.format(self.name),
                                                   ds_action=DSAction.DISPLAY_LOG.value))
                if self.repeatable:
                    self.status = ExpectationStatus.NOT_STARTED
                    agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                       ds_action_by='Dialogue System',
                                                       message='Expectation {} can be repeated again now!'.format(self.name),
                                                       ds_action=DSAction.DISPLAY_LOG.value))

    def get_next_not_executed_action(self):
        if len(self.steps_left) == 0:
            return None
        else:
            return self.steps_left[0].action

    def __repr__(self):
        return self.name
