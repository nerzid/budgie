from typing import List

from socialds.conditions.condition import Condition
from socialds.states.state import State


class AnyState(State):
    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs) -> List[Condition]:
        return []
