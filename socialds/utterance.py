from copy import deepcopy
from typing import List
import uuid

from socialds.action.action_obj import ActionObj


class Utterance:
    def __init__(
        self,
        text: str,
        actions: List[ActionObj],
        pronouns=None,
        alternatives=None,
    ):
        if pronouns is None:
            pronouns = []
        if alternatives is None:
            alternatives = []
        self.id = str(uuid.uuid4())
        self.pronouns = pronouns
        self.text = text
        self.actions = actions
        self.alternatives = alternatives

    # def get_actions_text(self):
    #

    def get_text_with_alternatives(self):
        text_with_alternatives = deepcopy(self.alternatives)
        text_with_alternatives.append(self.text)
        return text_with_alternatives

    def __repr__(self):
        action_str = ""
        for action in self.actions:
            action_str += "%s " % action
        action_str = action_str[:-1].replace("'", "")
        return "%s (%s)" % (self.text, action_str)
