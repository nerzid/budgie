from operations.operation import Operation


# this operation for the acts that cannot (or not yet) be lowered down to State Operations.
class SimpleAct(Operation):
    def __init__(self, name: str):
        super().__init__(name=name)

    def execute(self, *args, **kwargs):
        super().execute(*args, **kwargs)
        print(f'act({self.name}) executed')
