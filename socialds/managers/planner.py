from copy import copy
from typing import List
import logging
from socialds.action.effects.effect import Effect
from socialds.action.effects.functional.add_expected_action import AddExpectedAction
from socialds.action.effects.functional.add_expected_effect import AddExpectedEffect
from socialds.action.effects.functional.change_place import ChangePlace
from socialds.action.effects.functional.gain_knowledge import GainKnowledge
from socialds.action.effects.functional.move_knowledge import MoveKnowledge
from socialds.any.any_place import AnyPlace
from socialds.conditions.action_on_property_happens import ActionOnPropertyHappens
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.agent_does import AgentDoes
from socialds.conditions.agent_knows import AgentKnows
from socialds.conditions.condition_solution import ConditionSolution
from socialds.conditions.expectation_status_is import ExpectationStatusIs
from socialds.conditions.object_at_place import ObjectAtPlace
from socialds.expectation import ExpectationStatus
from socialds.managers.session_manager import SessionManager
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.variables import utterances
from socialds.plan import Plan
from socialds.relationstorage import RSType
from socialds.utterance import Utterance


class NoMatchingUtteranceFound(Exception):
    def __init__(self):
        super().__init__("No matching utterance with the given action or effects list is found")


class Planner:
    def __init__(self, agent):
        self.agent = agent
        self.solutions = None
        self.active_plans: List[Plan] = []

    # def plan(self, goal: Goal) -> Plan:
    #     """
    #
    #     Based on a goal or list of goals, plan chooses and initializes series of actions that can
    #     reach the goal. Since a goal is composed of list of conditions, the purpose of the plan method
    #     is to come up with a series of actions that will satisfy all the conditions of the goal.
    #     In other words, all the conditions of the goal must be satisfied (hold true) after the plan
    #     is executed
    #
    #     :param: goal: Goal to be satisfied using the returned plan
    #     :rtype: Plan returns the plan needed to satisfy the condition of the given goal
    #     """
    #     conditions = goal.conditions
    #     actions = []
    #     plan = Plan(goal=goal)
    #     for condition in conditions:
    #         pass
    #     print(managers.session_manager.get_sessions_info())

    def plan(self):
        """
        Creates plans for the available goals
        """
        ongoing_sessions = SessionManager.get_all_ongoing_sessions()

        all_goals = []
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
        for goal in all_goals:
            if goal.is_reached():
                continue
            else:
                # all_conditions.extend(goal.conditions)
                all_conditions = goal.conditions
                break
        condition_solutions = []
        for condition in all_conditions:
            if condition.check():
                continue
            if isinstance(condition, AgentDoes):
                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by performing the specific action',
                                      steps=[condition.action])
                )

                action = copy(condition.action)
                action.switch_done_by_with_recipient_if_not_pronoun()
                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by requesting other agent to do it',
                                      steps=[
                                          AddExpectedAction(action=action,
                                                            negation=False,
                                                            affected=DSTPronoun.YOU)
                                      ])
                )
            elif isinstance(condition, AgentKnows):
                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by learning it',
                                      steps=[
                                          GainKnowledge(condition.knows,
                                                        affected=DSTPronoun.I)])
                )

                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by remembering it',
                                      steps=[
                                          MoveKnowledge(knowledge=condition.knows,
                                                        from_rs=condition.agent.relation_storages[RSType.FORGOTTEN],
                                                        to_rs=condition.agent.relation_storages[RSType.KNOWLEDGEBASE],
                                                        affected=condition.agent)])
                )

                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by learning it from another agent',
                                      steps=[
                                          AddExpectedEffect(GainKnowledge(knowledge=condition.knows,
                                                                          affected=condition.agent),
                                                            negation=condition.negation,
                                                            affected=DSTPronoun.YOU)
                                      ])
                )
            elif isinstance(condition, AgentAtPlace):
                condition_solutions.append(
                    ConditionSolution(condition=condition,
                                      desc='by moving to the place',
                                      steps=[
                                          ChangePlace(from_place=AnyPlace(),
                                                      to_place=condition.place,
                                                      affected=condition.agent)
                                      ])
                )
            elif isinstance(condition, ObjectAtPlace):
                pass
            elif isinstance(condition, ActionOnPropertyHappens):
                pass
            elif isinstance(condition, ExpectationStatusIs):
                expectation = condition.expectation
                desired_status = condition.expectation_status
                if expectation.status == ExpectationStatus.NOT_STARTED or ExpectationStatus.ONGOING:
                    if desired_status == ExpectationStatus.COMPLETED:
                        condition_solutions.append(
                            ConditionSolution(condition=condition,
                                              desc='by performing the actions in the sequence',
                                              steps=[
                                                  condition.expectation.get_next_not_executed_action()
                                              ]))

        # print('Removing the impossible solutions')
        solutions = self.filter_out_the_solutions_without_competences(condition_solutions)
        return solutions

    def filter_out_the_solutions_without_competences(self, solutions: List[ConditionSolution]):
        """
        Removes the solutions that cannot be executed by the agent if the agent doesn't have the competence for it
        @param solutions:
        @return:
        """
        possible_actions, possible_effects = self.get_possible_actions_and_effects()

        # exclude the actions based on something, probably sessions? or preconditions?
        # write the that code here

        # select the actions based on the condition solutions
        # we check each solution and the required actions in them
        # if the agent can perform the actions needed in the solution, the solution stays
        # otherwise the solution is excluded from the solutions list
        # this means that we only keep the solutions that can be performed by the agent

        excluded_solutions = []
        for solution in solutions:
            exclude_solution = False
            for step in solution.steps:
                from socialds.action.action import Action
                from socialds.action.effects.effect import Effect
                if isinstance(step, Action):
                    if step not in possible_actions:
                        exclude_solution = True
                        break
                elif isinstance(step, Effect):
                    if step not in possible_effects:
                        exclude_solution = True
                        break
            if exclude_solution:
                excluded_solutions.append(solution)
        for excluded_solution in excluded_solutions:
            solutions.remove(excluded_solution)

        return solutions

    def get_possible_actions_and_effects(self):
        """
        Returns list of actions that are possible to use for pursuing activate plans
        """
        possible_actions = []
        possible_effects = []
        competences = self.agent.relation_storages[RSType.COMPETENCES].relations
        for competence in competences:
            possible_actions.append(competence.action)
            possible_effects.extend(competence.action.base_effects)
            possible_effects.extend(competence.action.extra_effects)
        return possible_actions, possible_effects

    def get_possible_utterances_with_solutions(self, solutions: List[ConditionSolution]):
        possible_utterances_with_solutions = []
        possible_actions, possible_effects = self.get_possible_actions_and_effects()
        logging.debug(f'Possible actions: {possible_actions}')
        logging.debug(f'Possible effects: {possible_effects}')

        from socialds.action.action import Action

        # checks if there are any utterance that contains all the solution steps in it
        # in other words, it looks for a single utterance that the goal of the agent can be reached
        for solution in solutions:
            for utterance in utterances:
                agent_can_do_all_actions_in_utterance = True
                actions = []
                effects = []
                # checks if the agent can do all the actions in the utterance
                # if not, then the agent cannot choose that utterance
                for action in utterance.actions:
                    if isinstance(action, Action):
                        # if the agent cannot perform an action inside the utterance
                        # then check if there are effects that can be performed instead
                        actions.append(action)
                        effects.extend(action.base_effects)
                        effects.extend(action.extra_effects)
                        if action not in possible_actions:
                            for effect in effects:
                                if effect not in possible_effects:
                                    agent_can_do_all_actions_in_utterance = False
                                    break
                if not agent_can_do_all_actions_in_utterance:
                    continue

                utterance_has_all_steps = True
                # the conditions here basically checks if there is an utterance
                # that contains all the steps in it.
                for step in solution.steps:
                    if isinstance(step, Action) and step not in actions:
                        utterance_has_all_steps = False
                        break
                    if isinstance(step, Effect) and step not in effects:
                        utterance_has_all_steps = False
                        break
                if utterance_has_all_steps:
                    possible_utterances_with_solutions.append((utterance, solution))
                    continue

                # checks if there are any matching utterances that contains the first solution step
                for step in solution.steps:
                    if isinstance(step, Action) and step in actions:
                        possible_utterances_with_solutions.append((utterance, solution))
                    if isinstance(step, Effect) and step in effects:
                        possible_utterances_with_solutions.append((utterance, solution))
        if len(possible_utterances_with_solutions) == 0:
            logging.debug(solutions)
            raise NoMatchingUtteranceFound
        else:
            return possible_utterances_with_solutions

    def get_the_best_matching_utterance_with_solution(self, solutions: List[ConditionSolution]):
        utts_with_solutions = self.get_possible_utterances_with_solutions(solutions)
        if len(utterances) > 0:
            return utts_with_solutions[0]
