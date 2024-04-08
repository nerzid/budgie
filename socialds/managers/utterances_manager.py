from typing import List

from socialds.action.action import Action
from socialds.agent import Agent
from socialds.utterance import Utterance


class UtterancesManager:
    def __init__(self, utterances: List[Utterance]):
        self.utterances = utterances

    def get_utterance_by_action(self, actions, checker: Agent):
        for utt in self.utterances:
            utt_match = True
            for action in actions:
                match = False

                action_count = 0
                for act in utt.actions:
                    if isinstance(act, Action):
                        action_count += 1

                if len(actions) != action_count:
                    utt_match = False
                    break

                for act in utt.actions:
                    if action.equals_with_pronouns(act, pronouns=checker.pronouns):
                        match = True
                if not match:
                    utt_match = False
                    break
            if utt_match:
                return utt
        return None
