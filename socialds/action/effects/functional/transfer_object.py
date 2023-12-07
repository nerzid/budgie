from socialds.action.effects.effect import Effect, EffectType


class TransferObject(Effect):
    def __init__(self):
        super().__init__(name='transfer-object', etype=EffectType.FUNCTIONAL, op_seq=[])
