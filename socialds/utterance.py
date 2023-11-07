from typing import List

from socialds.actions.action import ActionObj


class Utterance:
    def __init__(self, text: str, actions: List[ActionObj]):
        self.text = text
        self.actions = actions

    # def get_actions_text(self):
    #

    def __repr__(self):
        action_str = ''
        for action in self.actions:
            action_str += str(action.colorless_repr())
        return f'{self.text} ({action_str})'
