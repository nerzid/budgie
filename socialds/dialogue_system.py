import copy

import eventlet
from eventlet.greenpool import GreenPool
from socialds.action.action_operator import ActionOperator
from socialds.enums import DSActionByType, DSAction, Tense
from socialds.message import Message
from socialds.other.dst_pronouns import DSTPronoun
from socialds.other.event_listener import EventListener
from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RType


class DialogueSystem:
    def __init__(self, agent, auto_reaction_time=1):
        self.agent = agent
        self.auto_reaction_time = auto_reaction_time  # in seconds

        self.action_history = RelationStorage('Action History')
        self.dialogue_history = RelationStorage('Dialogue History')
        self.last_turn_actions = None

        self.on_agent_chose_utterance = EventListener()
        self.on_agent_executed_action = EventListener()
        self.on_agent_executed_last_action_from_utterance = EventListener()
        self.on_agent_executed_all_actions_from_utterance = EventListener()

    def act(self, beneficiary, utterance=None, actions=None):
        self.agent.pronouns[DSTPronoun.YOU] = beneficiary
        if self.agent.auto:
            self.run_auto_agent()
        elif utterance is not None:
            self.choose_utterance(utterance)
        elif actions is not None:
            self.choose_actions(actions)

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
        copied_utt = copy.deepcopy(utterance)
        eventlet.spawn(self.execute_actions, copied_utt.actions)

    def choose_actions(self, actions):
        action_pretty_string = ''
        for action in actions:
            action_pretty_string += str(action) + '\n'
        action_pretty_string = '<i>' + action_pretty_string + '</i>'
        self.agent.message_streamer.add(Message(ds_action_by_type=DSActionByType.AGENT.value,
                                                ds_action_by=self.agent.name,
                                                message=action_pretty_string,
                                                ds_action=DSAction.DISPLAY_UTTERANCE.value))
        eventlet.spawn(self.execute_actions, actions)

    def execute_actions(self, actions):
        # print('EXECUTING ACTIONS NOW for agent" {}'.format(self.agent))
        pool = eventlet.GreenPool()

        # executed_actions = []
        for action in actions:
            if isinstance(action, ActionOperator):
                continue
            # executed_actions.append(action)
            action.on_action_finished_executing.subscribe(self.add_action_to_action_history)
            pool.spawn(action.execute, self.agent)

        pool.waitall()
        self.on_agent_executed_all_actions_from_utterance.invoke(self.agent, actions)

    def add_action_to_action_history(self, agent, action):
        self.action_history.add(Relation(left=agent,
                                         rtype=RType.ACTION,
                                         rtense=Tense.PAST,
                                         right=action))

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
