from operations.operation import Operation


class StateOperation(Operation):
    def __init__(self, name: str):
        super().__init__(name=name)

    def execute(self):
        super().execute()
