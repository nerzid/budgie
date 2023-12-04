from socialds.operations.operation import Operation


class StateOperation(Operation):
    def __init__(self, name: str):
        super().__init__(name=name)

    def execute(self):
        super().execute()

    def execute_param_state_operations(self):
        pass
