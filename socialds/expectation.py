from copy import copy
from enum import Enum
from typing import List

from socialds.action.action_obj import ActionObj
from socialds.enums import Priority, Tense, DSAction, DSActionByType
from socialds.expectation_step import ExpectationStep
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun


class ExpectationType(Enum):
    NORM = "norm"
    STRATEGY = "strategy"


class ExpectationStatus(Enum):
    NOT_STARTED = "NOT STARTED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Expectation:
    def __init__(
        self,
        name: str,
        etype: ExpectationType,
        status: ExpectationStatus,
        steps: List[ExpectationStep],
        repeatable=False,
        priority: Priority = Priority.MID,
    ):
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
        self.priority = priority
        self.steps_left = copy(steps)
        self.steps_done = []
        self.step_symbols = {}
        self.step_agent_to_symbols = {}
        self.agent_id_to_agent = {}
        for step in steps:
            self.step_symbols[step.done_by] = None

    def update_status(self, agent):
        steps_to_be_removed = []
        if agent.id in self.step_agent_to_symbols:
            agent_symbol = self.step_agent_to_symbols[agent.id]
        else:
            agent_symbol = None

        if len(self.steps_left) == 0:
            return
        step = self.steps_left[0]
        is_to_be_removed = False

        from socialds.action.action import Action

        action = step.action
        if isinstance(action, Action):
            from socialds.states.relation import Relation
            from socialds.states.relation import RType

            # check if the agent did the action in last turn
            if agent.dialogue_system.last_turn_actions.contains(
                Relation(
                    left=agent, rtype=RType.ACTION, rtense=Tense.ANY, right=action
                ),
                agent.pronouns,
            ):
                # if the agent isn't assigned a symbol and
                # if the step's done_by symbol isn't assigned to any agent
                # then the agent can do the step
                if (
                    agent_symbol is None and self.step_symbols[step.done_by] is None
                ) or (step.done_by == agent_symbol):
                    is_to_be_removed = True
                    self.step_symbols[step.done_by] = agent.id
                    self.step_agent_to_symbols[agent.id] = step.done_by
                    self.agent_id_to_agent[agent.id] = agent
                    recipient = action.recipient
                    if isinstance(recipient, DSTPronoun):
                        recipient = agent.pronouns[recipient]
                    self.step_symbols[step.recipient] = recipient.id
                    self.step_agent_to_symbols[recipient.id] = step.recipient
                    self.agent_id_to_agent[recipient.id] = recipient
                    self.update_symbols_for_actions_in_steps()
                # for step_to_be_removed in steps_to_be_removed:
                #     if action.equals_with_pronouns(
                #         step_to_be_removed.action, agent.pronouns
                #     ):

                #         pass
                # if self.step_symbols[step.agent] == agent:
                #     is_to_be_removed = True
                # elif self.step_symbols[step.done_by] is None:
                #     # check if the agent is already associated with a symbol
                #         self.step_symbols[step.done_by] = agent
                #         is_to_be_removed = True

        if is_to_be_removed:
            self.steps_left.remove(step)
            self.steps_done.append(step)
        if len(self.steps_left) == 0:
            if self.status is not ExpectationStatus.COMPLETED:
                self.status = ExpectationStatus.COMPLETED
                agent.message_streamer.add(
                    Message(
                        ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                        ds_action_by="Dialogue System",
                        message="Expectation {} is completed!".format(self.name),
                        ds_action=DSAction.DISPLAY_LOG.value,
                    )
                )
                if self.repeatable:
                    self.status = ExpectationStatus.NOT_STARTED
                    agent.message_streamer.add(
                        Message(
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            ds_action_by="Dialogue System",
                            message="Expectation {} can be repeated again now!".format(
                                self.name
                            ),
                            ds_action=DSAction.DISPLAY_LOG.value,
                        )
                    )
            elif self.status is ExpectationStatus.COMPLETED:
                pass
            else:
                self.status = ExpectationStatus.FAILED
                agent.message_streamer.add(
                    Message(
                        ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                        ds_action_by="Dialogue System",
                        message="Expectation {} is failed!".format(self.name),
                        ds_action=DSAction.DISPLAY_LOG.value,
                    )
                )
                if self.repeatable:
                    self.status = ExpectationStatus.NOT_STARTED
                    agent.message_streamer.add(
                        Message(
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            ds_action_by="Dialogue System",
                            message="Expectation {} can be repeated again now!".format(
                                self.name
                            ),
                            ds_action=DSAction.DISPLAY_LOG.value,
                        )
                    )

    def update_symbols_for_actions_in_steps(self):
        for step in self.steps_left:
            if self.step_symbols[step.done_by] is not None:
                step.action.done_by = self.agent_id_to_agent[
                    self.step_symbols[step.done_by]
                ]
            if self.step_symbols[step.recipient] is not None:
                step.action_recipient = self.agent_id_to_agent[
                    self.step_symbols[step.recipient]
                ]

    def check_if_agent_pronouns_fits_symbols(self, agent):
        pronouns = agent.pronuns
        symbol_agent = self.step_agent_to_symbols[agent]

    def get_next_step(self) -> ExpectationStep:
        if len(self.steps_left) == 0:
            return None
        else:
            return self.steps_left[0]

    def get_next_not_executed_action(self):
        if len(self.steps_left) == 0:
            return None
        else:
            return self.steps_left[0].action

    def __repr__(self):
        return self.name
