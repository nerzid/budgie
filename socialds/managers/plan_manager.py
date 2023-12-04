from typing import List

import socialds.managers.managers as managers
from socialds.goal import Goal
from socialds.plan import Plan



class PlanManager:
    def __init__(self):
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
        pass
