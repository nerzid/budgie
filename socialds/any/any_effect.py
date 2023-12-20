from socialds.action.effects.effect import Effect
from socialds.any.any_object import AnyObject


class AnyEffect(Effect, AnyObject):
    def __init__(self):
        from socialds.any.any_agent import AnyAgent
        Effect.__init__(self, name='any-effect', from_state=[], to_state=[], affected=AnyAgent(), op_seq=[])
        AnyObject.__init__(self)

    def __eq__(self, other):
        if isinstance(other, Effect):
            return True
        return False
