import copy

import eventlet
from eventlet.greenpool import GreenPool
from socialds.action.action_operator import ActionOperator
from socialds.enums import DSActionByType, DSAction
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.event_listener import EventListener


class DialogueSystem:
    def __init__(self, agent, auto_reaction_time=1):
        self.agent = agent
        self.auto_reaction_time = auto_reaction_time  # in seconds

        self.action_history = None
        self.dialogue_history = None
        self.last_turn_actions = None

        self.on_agent_chose_utterance = EventListener()
        self.on_agent_executed_action = EventListener()
        self.on_agent_executed_last_action_from_utterance = EventListener()
        self.on_agent_executed_all_actions_from_utterance = EventListener()

    def act(self, beneficiary, utterance=None):
        self.agent.pronouns[DSTPronoun.YOU] = beneficiary
        if self.agent.auto:
            self.run_auto_agent()
        else:
            self.choose_utterance(utterance)

    def run_auto_agent(self):
        eventlet.sleep(self.auto_reaction_time)
        selected_utt, solution = self.agent.planner.get_the_best_matching_utterance_with_solution(
            self.agent.planner.plan())
        self.choose_utterance(selected_utt)

    def choose_utterance(self, utterance):
        self.on_agent_chose_utterance.invoke(agent=self.agent, utterance=utterance)
        self.agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.AGENT.value,
                                                ds_action_by=self.agent.name,
                                                message=utterance.text,
                                                ds_action=DSAction.DISPLAY_UTTERANCE.value))
        eventlet.spawn(self.execute_actions_of_utterance, utterance)

    def execute_actions_of_utterance(self, utterance):
        # print('EXECUTING ACTIONS NOW for agent" {}'.format(self.agent))
        pool = eventlet.GreenPool()
        copied_utt = copy.deepcopy(utterance)
        actions = []
        for action in copied_utt.actions:
            if isinstance(action, ActionOperator):
                continue
            actions.append(action)
            pool.spawn(action.execute, self.agent)
            self.on_agent_executed_action.subscribe(action.on_action_finished_executing)

        pool.waitall()
        self.on_agent_executed_all_actions_from_utterance.invoke(self.agent, actions)

    def get_planned_utterances(self):
        utts_str = []
        possible_utterances_with_solutions = self.agent.planner.get_possible_utterances_with_solutions(
            self.agent.planner.plan())
        for utt in possible_utterances_with_solutions:
            utts_str.append(str(utt[0]))
        self.agent.message_streamer.add(Message(ds_action=DSAction.REQUEST_USER_CHOOSE_UTTERANCE.value,
                                                ds_action_by=DSActionByType.DIALOGUE_SYSTEM.value,
                                                ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                message=utts_str))
