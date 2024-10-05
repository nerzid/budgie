from copy import deepcopy
from typing import List
import uuid

from socialds.action.action_obj import ActionObj
from socialds.other.unique_id_generator import get_unique_id


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
        self.id = get_unique_id()
        self.pronouns = pronouns
        self.text = text
        self.actions = actions
        self.alternatives = alternatives

    # def get_actions_text(self):
    #

    def clone(self):
        return deepcopy(self)
        # cloned_actions = []
        # for action in self.actions:
        #     cloned_actions.append(deepcopy(action))
        # return Utterance(self.text, cloned_actions, self.pronouns, self.alternatives)


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

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "text": self.text,
            "actions": [action.to_dict() for action in self.actions],
            "alternatives": [alternative.to_dict() for alternative in self.alternatives],
        }