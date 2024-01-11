from socialds.operations.operation import Operation


class StateOperation(Operation):
    def __init__(self, name: str):
        super().__init__(name=name)

    def execute(self, pronouns, *args, **kwargs):
        super().execute(pronouns)

    def execute_param_state_operations(self):
        pass
