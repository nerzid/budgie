from socialds.action.effects.effect import Effect, EffectType


class Need(Effect):
    def __init__(self, ):
        super().__init__(name='need', etype=EffectType.SOCIAL, op_seq=[])
