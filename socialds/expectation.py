from copy import copy
from enum import Enum
from typing import List

from socialds.action.action_obj import ActionObj
from socialds.conditions.condition import Condition
from socialds.enums import PlaceholderSymbol, Priority, Tense, DSAction, DSActionByType
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
        starting_conditions: List[Condition],
        symbol_values: dict,
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
        self.starting_conditions = starting_conditions
        self.symbol_values = symbol_values
        self.etype = etype
        self.status = status
        self.step = steps
        self.priority = priority
        self.steps_left = copy(steps)
        self.steps_done = []
        self.symbol_to_id = {}
        self.id_to_symbol = {}
        self.id_to_object = {}
        for step in steps:
            self.symbol_to_id[step.done_by] = None

    def update_status(self, agent):
        steps_to_be_removed = []
        if agent.id in self.id_to_symbol:
            agent_symbol = self.id_to_symbol[agent.id]
        else:
            agent_symbol = None

        if len(self.steps_left) == 0:
            return
        step = self.steps_left[0]
        is_to_be_removed = False

        from socialds.action.action import Action

        # Get all the actions that has the same name with the step.action
        found_actions = []
        for action_relation in agent.dialogue_system.last_turn_actions.relations:
            if type(action_relation.right) == step.action:
                found_actions.append(action_relation.right)

        matched_actions = []
        # Check if all attributes besides placeholders are equal
        for found_action in found_actions:
            matched = True
            for key, value in step.action_attrs.items():
                if isinstance(value, PlaceholderSymbol):
                    pass
                else:
                    attribute = getattr(found_action, key)
                    # check if either values are same
                    # it checks if it is the same object first, if not, it checks through equals_with_pronouns
                    # e.g., if one is DSTPronoun.I and the other is Jane(doctor), it needs to use equals_with_pronouns
                    # e.g., if both of them are Jane(doctor), then attribute == value would work as they refer to the same object
                    if attribute == value or (
                        hasattr(attribute, "equals_with_pronouns")
                        and callable(attribute.equals_with_pronouns)
                        and attribute.equals_with_pronouns(value, agent.pronouns)
                    ):
                        continue
                    else:
                        # if the attributes are not matching, then these only share the same action types but different actions
                        # e.g., once action can be sharing X and the other can be sharing Y which are different.
                        matched = False
            if matched:
                matched_actions.append(found_action)

        for matched_action in matched_actions:
            for key, value in step.action_attrs.items():
                if isinstance(value, PlaceholderSymbol):
                    attribute = getattr(matched_action, key)
                    self.symbol_to_id[value] = attribute.id
                    self.id_to_symbol[attribute.id] = value
                    self.id_to_object[attribute.id] = attribute
                    step.action_attrs[key] = attribute

            break
            # TODO figure out how to do it if the agent does more than one matching actions.
            # e.g., the patient can worry about two different things, which means that two different norms must be started and responded to
        if len(matched_actions) > 0:
            action = step.action(**step.action_attrs)
            # if isinstance(action, Action):
            #     from socialds.states.relation import Relation
            #     from socialds.states.relation import RType

            #     # check if the agent did the action in last turn
            #     if agent.dialogue_system.last_turn_actions.contains(
            #         Relation(
            #             left=agent, rtype=RType.ACTION, rtense=Tense.ANY, right=action
            #         ),
            #         agent.pronouns,
            #     ):
            #         # if the agent isn't assigned a symbol and
            #         # if the step's done_by symbol isn't assigned to any agent
            #         # then the agent can do the step
            if (agent_symbol is None and self.symbol_to_id[step.done_by] is None) or (
                step.done_by == agent_symbol
            ):
                is_to_be_removed = True
                self.symbol_to_id[step.done_by] = agent.id
                self.id_to_symbol[agent.id] = step.done_by
                self.id_to_object[agent.id] = agent
                recipient = action.recipient
                if isinstance(recipient, DSTPronoun):
                    recipient = agent.pronouns[recipient]
                self.symbol_to_id[step.recipient] = recipient.id
                self.id_to_symbol[recipient.id] = step.recipient
                self.id_to_object[recipient.id] = recipient
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

            if (
                len(self.steps_left) != 0
                and len(self.steps_done) != 0
                and self.status == ExpectationStatus.NOT_STARTED
            ):
                self.status = ExpectationStatus.ONGOING

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
            if self.symbol_to_id[step.done_by] is not None:
                step.action.done_by = self.id_to_object[self.symbol_to_id[step.done_by]]
            if self.symbol_to_id[step.recipient] is not None:
                step.action_recipient = self.id_to_object[
                    self.symbol_to_id[step.recipient]
                ]

    def check_if_agent_pronouns_fits_symbols(self, agent):
        pronouns = agent.pronuns
        symbol_agent = self.id_to_symbol[agent]

    def get_next_step(self) -> ExpectationStep:
        if len(self.steps_left) == 0:
            return None
        else:
            step = self.steps_left[0]
            for key, value in step.action_attrs.items():
                if isinstance(value, PlaceholderSymbol):
                    step.action_attrs[key] = self.id_to_object[self.symbol_to_id[value]]
            return step

    def get_next_not_executed_action(self):
        if len(self.steps_left) == 0:
            return None
        else:
            return self.steps_left[0].action

    def __repr__(self):
        return self.name
