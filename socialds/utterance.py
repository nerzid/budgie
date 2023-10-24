from typing import List

from actions.action import Action


class Utterance:
    def __init__(self, text: str, actions: List[Action]):
        self.text = text
        self.actions = actions

    def __str__(self):
        return f'{self.text} ({self.actions})'
