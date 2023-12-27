from typing import List

from socialds.action.action_obj import ActionObj


class Utterance:
    def __init__(self, text: str, actions: List[ActionObj]):
        self.text = text
        self.actions = actions

    # def get_actions_text(self):
    #


    def __repr__(self):
        action_str = ''
        for action in self.actions:
            action_str += "%r " % action
        action_str = action_str[:-1]
        return "%s (%s)" % (self.text, action_str)
