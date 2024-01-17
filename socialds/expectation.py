from copy import copy
from enum import Enum
from typing import List

import socialds.other.variables as vars
from socialds.action.action_obj import ActionObj
from socialds.enums import Tense, DSAction, DSActionByType
from socialds.states.relation import Relation, RType


class ExpectationType(Enum):
    NORM = 'norm'
    STRATEGY = 'strategy'


class ExpectationStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class Expectation:
    def __init__(self, name: str, etype: ExpectationType, status: ExpectationStatus, action_seq: List[ActionObj]):
        """
        Creates an expectation of an action sequence that is expected to be seen during the dialogue.
        For example, norms are type of expectations that are expected to be performed by the agents
        There are various norms such as cultural norms, social norms, etc.
        @param name:
        @param etype:
        @param status:
        @param action_seq:
        """
        self.name = name
        self.etype = etype
        self.status = status
        self.action_seq = action_seq
        self.actions_left = copy(action_seq)
        self.actions_done = []

    def update_status(self, agent):
        from socialds.managers.managers import message_streamer
        actions_to_removed = []
        for action in self.actions_left:
            from socialds.action.action import Action
            if isinstance(action, Action):
                if action.is_action_in_list(vars.last_turn_actions, agent.pronouns) \
                        and not action.is_action_in_list(actions_to_removed, agent.pronouns):
                    actions_to_removed.append(action)
                    self.status = ExpectationStatus.ONGOING
                    continue
        for action in actions_to_removed:
            self.actions_left.remove(action)
            self.actions_done.append(action)
        if len(self.actions_left) == 0:
            if self.status is not ExpectationStatus.COMPLETED:
                self.status = ExpectationStatus.COMPLETED
                message_streamer.add(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                     ds_action_by='Dialogue System',
                                     message='Expectation {} is completed!'.format(self.name),
                                     ds_action=DSAction.DISPLAY_LOG.value)
            elif self.status is ExpectationStatus.COMPLETED:
                pass
            else:
                self.status = ExpectationStatus.FAILED
                message_streamer.add(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                     ds_action_by='Dialogue System',
                                     message='Expectation {} is failed!'.format(self.name),
                                     ds_action=DSAction.DISPLAY_LOG.value)

    def get_next_not_executed_action(self):
        if len(self.actions_left) == 0:
            if self.status is not ExpectationStatus.FAILED:
                self.status = ExpectationStatus.COMPLETED
                message_streamer.add(ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                     ds_action_by='Dialogue System',
                                     message='Expectation {} is completed!'.format(self.name),
                                     ds_action=DSAction.DISPLAY_LOG.value)
            return None
        else:
            return self.actions_left[0]

    def __repr__(self):
        return self.name
