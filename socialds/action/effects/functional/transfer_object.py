from socialds.action.effects.effect import Effect


class TransferObject(Effect):
    def __init__(self, affected: any):
        super().__init__('transfer-object', [], [], affected, [])
