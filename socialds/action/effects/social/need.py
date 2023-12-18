from socialds.action.effects.effect import Effect
from socialds.other.dst_pronouns import DSTPronoun


class Need(Effect):
    def __init__(self):
        super().__init__(name='need', from_state=[], to_state=[], affected=DSTPronoun.I, op_seq=[])