from copy import copy, deepcopy
from typing import List
import logging

from numpy import isin


from socialds.action.effects.effect import Effect
from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.functional.change_place import ChangePlace
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.effects.functional.move_knowledge import MoveInformation
from socialds.action.effects.social.gain_permit import GainPermit
from socialds.any.any_object import AnyObject
from socialds.any.any_place import AnyPlace
from socialds.conditions.IsRelationInRelationStorage import IsRelationInRelationStorage
from socialds.conditions.action_on_property_happens import ActionOnResourceHappens
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.agent_does_action import AgentDoesAction
from socialds.conditions.agent_does_effect import AgentDoesEffect
from socialds.conditions.agent_does_one_of_the_actions import AgentDoesOneOfTheActions
from socialds.conditions.agent_knows import AgentKnows
from socialds.conditions.condition_solution import ConditionSolution
from socialds.conditions.expectation_status_is import ExpectationStatusIs
from socialds.conditions.object_at_place import ObjectAtPlace
from socialds.enums import Tense, DSAction, DSActionByType
from socialds.expectation import ExpectationStatus
from socialds.goal import Goal
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun
from socialds.plan import Plan
from socialds.relationstorage import RSType
from socialds.states.relation import Relation, RType


class NoMatchingUtteranceFound(Exception):
    def __init__(self):
        super().__init__(
            "No matching utterance with the given action or effects list is found"
        )


class Planner:
    def __init__(self, agent):
        self.agent = agent
        self.name = "{}'s Planner".format(self.agent)
        self.solutions = None
        self.active_plans: List[Plan] = []

    def plan(self):
        from socialds.action.actions.verbal.request_confirmation import (
            RequestConfirmation,
        )
        from socialds.action.actions.verbal.request_action import RequestAction

        """
        Creates plans for the available goals
        """
        ongoing_sessions = self.agent.session_manager.get_all_ongoing_sessions()

        all_goals: List[Goal] = []

        all_goals.extend(self.create_goals_from_expected_effects())
        all_goals.extend(self.create_goals_from_expected_actions())

        # Uncomment below when agent goals are implemented
        # all_goals = self.agent.goals

        session_goals = []
        for session in ongoing_sessions:
            session_goals.extend(session.end_goals)

        all_goals.extend(session_goals)
        all_conditions = []

        # At the moment, this code plans for one goal at a time.
        # Ideally, it should consider all the goals and plan accordingly
        # Instead, this code chooses the next unreached goal and plan for reaching that
        # After the goal is reached, it moves to next goal and plans accordingly
        # all_goals = all_goals + self.create_goals_from_expected_actions() + self.create_goals_from_expected_effects()
        for goal in all_goals:
            if goal.is_reached(self.agent):
                continue
            elif self.agent not in goal.known_by:
                continue
            else:
                # all_conditions.extend(goal.conditions)
                for condition in goal.conditions:
                    if not condition.check(self.agent):
                        all_conditions.append(condition)
                # break

        # from socialds.action.action import Action
        # expected_actions: List[Action] = []
        # expected_effects: List[Effect] = []
        # for expected_action_relation in self.agent.relation_storages[RSType.EXPECTED_ACTIONS]:
        #     expected_actions.append(expected_action_relation.right)
        # for expected_effect_relation in self.agent.relation_storages[RSType.EXPECTED_EFFECTS]:
        #     expected_effects.append(expected_effect_relation.right)

        condition_solutions = []
        plans = []
        for condition in all_conditions:
            if condition.check(self.agent):
                continue
            if isinstance(condition, AgentDoesAction):
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by performing the specific action",
                        steps=[condition.action],
                    )
                )
                plans.append(Plan(steps=[condition.action]))

                action = copy(condition.action)
                action.switch_done_by_with_recipient_if_not_pronoun()
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by requesting other agent to do it",
                        steps=[
                            AddExpectedAction(action=action, affected=DSTPronoun.YOU)
                        ],
                    )
                )
                plans.append(
                    Plan(
                        steps=[
                            AddExpectedAction(action=action, affected=DSTPronoun.YOU)
                        ]
                    )
                )
            elif isinstance(condition, AgentDoesOneOfTheActions):
                actions = []
                for action in condition.actions:
                    if action.check_preconditions(self.agent):
                        actions.append(action)
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by performing one of the actions, starting from the first one",
                        steps=actions,
                    )
                )
                plans.append(condition.actions)
            elif isinstance(condition, AgentKnows):
                if self.agent.equals_with_pronouns(
                    condition.agent, self.agent.pronouns
                ):
                    # condition_solutions.append(
                    #     ConditionSolution(
                    #         condition=condition,
                    #         desc="by learning it",
                    #         steps=[
                    #             GainKnowledge(condition.knows, affected=DSTPronoun.I)
                    #         ],
                    #     )
                    # )
                    # plans.append(
                    #     Plan([GainKnowledge(condition.knows, affected=DSTPronoun.I)])
                    # )
                    condition_solutions.append(
                        ConditionSolution(
                            condition=condition,
                            desc="by remembering it",
                            steps=[
                                MoveInformation(
                                    information=condition.knows,
                                    from_rs=condition.agent.relation_storages[
                                        RSType.FORGOTTEN
                                    ],
                                    to_rs=condition.agent.relation_storages[
                                        RSType.KNOWLEDGEBASE
                                    ],
                                    affected=condition.agent,
                                )
                            ],
                        )
                    )
                    plans.append(
                        Plan(
                            [
                                MoveInformation(
                                    information=condition.knows,
                                    from_rs=condition.agent.relation_storages[
                                        RSType.FORGOTTEN
                                    ],
                                    to_rs=condition.agent.relation_storages[
                                        RSType.KNOWLEDGEBASE
                                    ],
                                    affected=condition.agent,
                                )
                            ]
                        )
                    )
                    if isinstance(condition.knows.right, AnyObject):
                        # This condition checks if the information has a specific subject.
                        # E.g., if the agent wants to know whether the patient's eye is teary or not
                        # then the subject here is "teary", therefore the question should a requestconfirmation
                        # if the subject is an instance of anyobject such as anyproperty, the question can be
                        # asked with requestinfo e.g., if eye has something "eye -is-> any_property" or
                        # "eye -has-> any_property"
                        condition_solutions.append(
                            ConditionSolution(
                                condition=condition,
                                desc="by learning it from another agent",
                                steps=[
                                    AddExpectedEffect(
                                        GainKnowledge(
                                            knowledge=condition.knows,
                                            affected=condition.agent,
                                        ),
                                        negation=condition.negation,
                                        affected=DSTPronoun.YOU,
                                    )
                                ],
                            )
                        )

                        plans.append(
                            Plan(
                                [
                                    AddExpectedEffect(
                                        GainKnowledge(
                                            knowledge=condition.knows,
                                            affected=condition.agent,
                                        ),
                                        negation=condition.negation,
                                        affected=DSTPronoun.YOU,
                                    )
                                ]
                            )
                        )
                    else:
                        condition_solutions.append(
                            ConditionSolution(
                                condition=condition,
                                desc="by confirming it with an agent",
                                steps=[
                                    RequestConfirmation(
                                        done_by=DSTPronoun.I,
                                        asked=condition.knows,
                                        tense=Tense.ANY,
                                        recipient=DSTPronoun.YOU,
                                    )
                                ],
                            )
                        )
                        plans.append(
                            Plan(
                                [
                                    RequestConfirmation(
                                        done_by=DSTPronoun.I,
                                        asked=condition.knows,
                                        tense=Tense.ANY,
                                        recipient=DSTPronoun.YOU,
                                    )
                                ]
                            )
                        )
                else:
                    condition_solutions.append(
                        ConditionSolution(
                            condition=condition,
                            desc="by teaching it",
                            steps=[
                                GainKnowledge(
                                    knowledge=condition.knows, affected=condition.agent
                                )
                            ],
                        )
                    )

                    from socialds.action.actions.verbal.affirm import Affirm

                    condition_solutions.append(
                        ConditionSolution(
                            condition=condition,
                            desc="by confirming it",
                            steps=[
                                Affirm(
                                    affirmed=condition.knows,
                                    done_by=self.agent,
                                    recipient=condition.agent,
                                )
                            ],
                        )
                    )

                    from socialds.action.actions.verbal.deny import Deny

                    condition_solutions.append(
                        ConditionSolution(
                            condition=condition,
                            desc="by denying it",
                            steps=[
                                Deny(
                                    denied=condition.knows,
                                    done_by=self.agent,
                                    recipient=condition.agent,
                                )
                            ],
                        )
                    )
                    plans.append(
                        Plan(
                            [
                                GainKnowledge(
                                    knowledge=condition.knows, affected=condition.agent
                                )
                            ]
                        )
                    )
            elif isinstance(condition, AgentAtPlace):
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by moving to the place",
                        steps=[
                            ChangePlace(
                                from_place=AnyPlace(),
                                to_place=condition.place,
                                affected=condition.agent,
                            )
                        ],
                    )
                )
                plans.append(
                    Plan(
                        [
                            ChangePlace(
                                from_place=AnyPlace(),
                                to_place=condition.place,
                                affected=condition.agent,
                            )
                        ]
                    )
                )
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by asking for the permit to move to the place",
                        steps=[
                            RequestAction(
                                done_by=condition.agent,
                                requested=GainPermit(
                                    permit=Relation(
                                        left=condition.agent,
                                        rtype=RType.IS_PERMITTED_TO,
                                        rtense=Tense.PRESENT,
                                        right=ChangePlace(
                                            from_place=AnyPlace(),
                                            to_place=condition.place,
                                            affected=condition.agent,
                                        ),
                                    ),
                                    affected=condition.agent,
                                ),
                            )
                        ],
                    )
                )
                plans.append(
                    Plan(
                        [
                            ChangePlace(
                                from_place=AnyPlace(),
                                to_place=condition.place,
                                affected=condition.agent,
                            )
                        ]
                    )
                )
                condition_solutions.append(
                    ConditionSolution(
                        condition=condition,
                        desc="by giving permit to the agent to change his place",
                        steps=[
                            GainPermit(
                                permit=Relation(
                                    left=condition.agent,
                                    rtype=RType.IS_PERMITTED_TO,
                                    rtense=Tense.PRESENT,
                                    right=ChangePlace(
                                        from_place=AnyPlace(),
                                        to_place=condition.place,
                                        affected=condition.agent,
                                    ),
                                ),
                                affected=condition.agent,
                            )
                        ],
                    )
                )
                plans.append(
                    Plan(
                        [
                            GainPermit(
                                permit=Relation(
                                    left=condition.agent,
                                    rtype=RType.IS_PERMITTED_TO,
                                    rtense=Tense.PRESENT,
                                    right=ChangePlace(
                                        from_place=AnyPlace(),
                                        to_place=condition.place,
                                        affected=condition.agent,
                                    ),
                                ),
                                affected=condition.agent,
                            )
                        ]
                    )
                )
            elif isinstance(condition, ObjectAtPlace):
                pass
            elif isinstance(condition, ActionOnResourceHappens):
                pass
            elif isinstance(condition, ExpectationStatusIs):
                expectation = condition.expectation
                desired_status = condition.expectation_status
                if (
                    expectation.status == ExpectationStatus.NOT_STARTED
                    or ExpectationStatus.ONGOING
                ):
                    if desired_status == ExpectationStatus.COMPLETED:
                        action = condition.expectation.get_next_not_executed_action()
                        if action is not None:
                            condition_solutions.append(
                                ConditionSolution(
                                    condition=condition,
                                    desc="by performing the actions in the sequence",
                                    steps=[action],
                                )
                            )
                            plans.append(Plan([action]))

        # print('Removing the impossible solutions')
        solutions = self.filter_solutions_by_steps(condition_solutions)
        return solutions

    def create_goals_from_expected_actions(self):
        goals = []
        expected_actions = self.agent.relation_storages[RSType.EXPECTED_ACTIONS]
        for action in expected_actions:
            from socialds.action.action import Action

            if isinstance(action, Action):
                condition = AgentDoesAction(
                    agent=action.done_by, action=action, tense=Tense.ANY
                )
                goals.append(
                    Goal(
                        owner=self.agent,
                        name="goal for the expected action %s" % action,
                        conditions=[condition],
                        known_by=[self.agent],
                    )
                )
            elif isinstance(action, List):
                condition = AgentDoesOneOfTheActions(
                    agent=action[0].done_by, actions=action, tense=Tense.ANY
                )
                goals.append(
                    Goal(
                        owner=self.agent,
                        name="goal for the expected actions %s" % action,
                        conditions=[condition],
                        known_by=[self.agent],
                    )
                )
        self.agent.relation_storages[RSType.GOALS].add_multi(goals)
        self.clear_expected_actions()
        return goals

    def create_goals_from_expected_effects(self):
        goals = []
        conditions = []
        expected_actions = self.agent.relation_storages[RSType.EXPECTED_ACTIONS]
        expected_effects = self.agent.relation_storages[RSType.EXPECTED_EFFECTS]
        for effect_rel in expected_effects:
            condition = AgentDoesEffect(
                agent=DSTPronoun.I, effect=effect_rel.right, tense=Tense.ANY
            )
            goals.append(
                Goal(
                    owner=self.agent,
                    name="goal for the expected effect %s" % effect_rel.right,
                    conditions=[condition],
                    known_by=[self.agent],
                )
            )
        for action_rel in expected_actions:
            action = action_rel.right
            if isinstance(action, List):
                condition = AgentDoesOneOfTheActions(
                    agent=DSTPronoun.I, actions=action, tense=Tense.ANY
                )
                conditions.append(condition)
                goals.append(
                    Goal(
                        owner=self.agent,
                        name="goal for the expected one of the actions %s" % action,
                        conditions=conditions,
                        known_by=[self.agent],
                    )
                )
            else:
                if not action.specific:
                    effects = action.base_effects + action.extra_effects
                    for effect in effects:
                        condition = AgentDoesEffect(
                            agent=DSTPronoun.I, effect=effect, tense=Tense.ANY
                        )
                        conditions.append(condition)
                    goals.append(
                        Goal(
                            owner=self.agent,
                            name="goal for the expected action %s" % action,
                            conditions=conditions,
                            known_by=[self.agent],
                        )
                    )
        self.agent.relation_storages[RSType.GOALS].add_multi(goals)
        self.clear_expected_effects()
        return goals

    def filter_solutions_by_steps(self, solutions: List[ConditionSolution]):
        """
        Removes the solutions that cannot be executed by the agent if the agent doesn't have the competence for it
        @param solutions:
        @return:
        """
        print("{} ALL SOLUTIONS -> {}".format(self.agent, solutions))
        from socialds.action.action import Action
        from socialds.action.effects.effect import Effect

        possible_actions, possible_effects = self.get_possible_actions_and_effects()

        # exclude the actions based on something, probably sessions? or preconditions?
        # write the that code here

        # select the actions based on the condition solutions
        # we check each solution and the required actions in them
        # if the agent can perform the actions needed in the solution, the solution stays
        # otherwise the solution is excluded from the solutions list
        # this means that we only keep the solutions that can be performed by the agent

        # By competences
        excluded_solutions = []
        for solution in solutions:
            exclude_solution = False
            for step in solution.steps:
                if isinstance(step, Action):
                    if not step.is_action_in_list(
                        possible_actions, self.agent.pronouns
                    ):
                        print(
                            "{} step {} not in possible actions {}".format(
                                self.agent, step, possible_actions
                            )
                        )
                        exclude_solution = True
                        break
                elif isinstance(step, Effect):
                    # print(step.pronouns)
                    if not step.is_effect_in_list(
                        possible_effects, self.agent.pronouns
                    ):
                        print(
                            "{} step {} not in possible effects {}".format(
                                self.agent, step, possible_effects
                            )
                        )
                        exclude_solution = True
                        break
            if exclude_solution:
                excluded_solutions.append(solution)
        print(
            "{} SOLUTIONS to remove for competence filter-> {}".format(
                self.agent, excluded_solutions
            )
        )

        # By requirements
        # if the object has the requirement of certain conditions
        # and if the conditions are NOT satisfied, then the agent
        # cannot do that action
        for solution in solutions:
            exclude_solution = False
            for step in solution.steps:
                if isinstance(step, Action) or isinstance(step, Effect):
                    for requirement_holder in step.get_requirement_holders():
                        if requirement_holder is None:
                            continue
                        if isinstance(requirement_holder, DSTPronoun):
                            requirement_holder = self.agent.pronouns[requirement_holder]
                        for requirement in requirement_holder.relation_storages[
                            RSType.REQUIREMENTS
                        ]:
                            if requirement.required_for.equals_with_pronouns(
                                step, self.agent.pronouns
                            ):
                                if (
                                    not requirement.check(self.agent)
                                    and solution not in excluded_solutions
                                ):
                                    excluded_solutions.append(solution)
                                    break

        for excluded_solution in excluded_solutions:
            solutions.remove(excluded_solution)
        print("SOLUTIONS after requirement filter-> {}".format(solutions))
        return solutions

    def get_possible_actions_and_effects(self):
        """
        Returns list of actions that are possible to use for pursuing activate plans
        """
        possible_actions = []
        possible_effects = []
        competences = self.agent.relation_storages[RSType.COMPETENCES].relations
        permits = self.agent.relation_storages[RSType.PERMITS].relations
        for competence in competences:
            possible_actions.append(competence.action)
            possible_effects.extend(competence.action.base_effects)
            possible_effects.extend(competence.action.extra_effects)

        for permit in permits:
            from socialds.action.action import Action

            permitted = permit.right
            if isinstance(permitted, Action):
                possible_actions.append(permitted)
            elif isinstance(permitted, Effect):
                possible_effects.append(permitted)

        return possible_actions, possible_effects

    def get_possible_utterances_with_solutions(
        self, solutions: List[ConditionSolution]
    ):
        possible_utterances_with_solutions = []
        possible_actions, possible_effects = self.get_possible_actions_and_effects()
        logging.debug(f"Possible actions: {possible_actions}")
        logging.debug(f"Possible effects: {possible_effects}")

        from socialds.action.action import Action

        # checks if there are any utterances that contains all the solution steps in it
        # in other words, it looks for a single utterance that the goal of the agent can be reached
        for solution in solutions:
            for utterance in self.agent.utterances_manager.utterances:
                agent_can_do_all_actions_in_utterance = True
                actions = []
                effects = []
                # checks if the agent can do all the actions in the utterance
                # if not, then the agent cannot choose that utterance
                for action in utterance.actions:
                    if isinstance(action, Action):
                        if not action.check_preconditions(checker=self.agent):
                            agent_can_do_all_actions_in_utterance = False
                            break
                        # check if the actions in the utterance can be executed by the agent
                        requirement_holders = action.get_requirement_holders()
                        # print(action.name)
                        if requirement_holders is not None:
                            for requirement_holder in requirement_holders:
                                if requirement_holder is None:
                                    continue
                                if isinstance(requirement_holder, DSTPronoun):
                                    requirement_holder = self.agent.pronouns[
                                        requirement_holder
                                    ]
                                for requirement in requirement_holder.relation_storages[
                                    RSType.REQUIREMENTS
                                ]:
                                    if requirement.required_for.equals_with_pronouns(
                                        action, self.agent.pronouns
                                    ):
                                        if not requirement.check(self.agent):
                                            agent_can_do_all_actions_in_utterance = (
                                                False
                                            )
                                            break

                        # if the agent cannot perform an action inside the utterance
                        # then check if there are effects that can be performed instead
                        # copied_action = deepcopy(action)
                        # actions.append(copied_action)
                        # effects.extend(copied_action.base_effects)
                        # effects.extend(copied_action.extra_effects)

                        # might cause bugs
                        actions.append(action)
                        effects.extend(action.base_effects)
                        effects.extend(action.extra_effects)
                        if not action.is_action_in_list(
                            possible_actions, self.agent.pronouns
                        ):
                            for effect in effects:
                                if not effect.is_effect_in_list(
                                    possible_effects, self.agent.pronouns
                                ):
                                    agent_can_do_all_actions_in_utterance = False
                                    break
                if not agent_can_do_all_actions_in_utterance:
                    continue

                utterance_has_all_steps = True
                # the conditions here basically checks if there is an utterance
                # that contains all the steps in it.
                for step in solution.steps:
                    if isinstance(step, Action) and not step.is_action_in_list(
                        actions, self.agent.pronouns
                    ):
                        utterance_has_all_steps = False
                        break
                    if isinstance(step, Effect) and not step.is_effect_in_list(
                        effects, self.agent.pronouns
                    ):
                        utterance_has_all_steps = False
                        break
                if utterance_has_all_steps:
                    possible_utterances_with_solutions.append((utterance, solution))
                    continue

                # checks if there are any matching utterances that contains the first solution step
                for step in solution.steps:
                    if isinstance(step, Action) and step.is_action_in_list(
                        actions, self.agent.pronouns
                    ):
                        possible_utterances_with_solutions.append((utterance, solution))
                    if isinstance(step, Effect) and step.is_effect_in_list(
                        effects, self.agent.pronouns
                    ):
                        possible_utterances_with_solutions.append((utterance, solution))
        if len(possible_utterances_with_solutions) == 0:
            logging.debug(solutions)
            # self.agent.message_streamer.add(Message(ds_action=DSAction.DISPLAY_LOG.value,
            #                                         ds_action_by=self.name,
            #                                         ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
            #                                         message=self.agent.session_manager.get_sessions_info(self.agent)))
            raise NoMatchingUtteranceFound
        else:
            return possible_utterances_with_solutions

    def clear_expected_actions(self):
        self.agent.relation_storages[RSType.EXPECTED_ACTIONS].remove_all()

    def clear_expected_effects(self):
        self.agent.relation_storages[RSType.EXPECTED_EFFECTS].remove_all()

    def get_actions_from_plans(self, plans: List[ConditionSolution]):
        actions = []
        for plan in plans:
            for step in plan.steps:
                from socialds.action.action import Action

                if isinstance(step, Action):
                    actions.append(step)
                elif isinstance(step, Effect):
                    action = self.from_effects_to_actions([step])
                    if action is not None:
                        actions.extend(action)
        return actions

    def get_the_best_matching_utterance_with_solution(
        self, solutions: List[ConditionSolution]
    ):
        utts_with_solutions = self.get_possible_utterances_with_solutions(solutions)
        if len(self.agent.utterances_manager.utterances) > 0:
            return utts_with_solutions[0]

    def from_effects_to_actions(self, effects):
        """
        Returns the actions that have exactly the same list of effects.
        TODO Atm, it only returns one action,
        however, a better algorithm would go over each action that would result in the same list of effects and
        return those actions instead
        @param effects: @return:
        """
        possible_actions = []
        competences = self.agent.relation_storages[RSType.COMPETENCES].relations
        permits = self.agent.relation_storages[RSType.PERMITS].relations
        for competence in competences:
            possible_actions.append(competence.action)

        for permit in permits:
            from socialds.action.action import Action

            permitted = permit.right
            if isinstance(permitted, Action):
                possible_actions.append(permitted)

        for action in possible_actions:
            a_effects = action.base_effects
            # for c_effect in action.extra_effects:
            #     if c_effect.condition.check(self.agent):
            #         pass
            found_action = True
            for effect in effects:
                found_effect = False
                for a_effect in a_effects:
                    if effect.equals_with_pronouns(a_effect, self.agent.pronouns):
                        found_effect = True
                if not found_effect:
                    found_action = False
                    break
            if found_action:
                possible_action = action.__class__.build_instance_from_effects(
                    done_by=action.done_by,
                    recipient=action.recipient,
                    tense=action.tense,
                    negation=action.negation,
                    effects=effects,
                )
                if possible_action.check_preconditions(checker=self.agent):
                    return [possible_action]
        return None

        # if len(effects) == 1:
        #     if effects[0].equals_with_pronouns(effect, self.agent.pronouns):
