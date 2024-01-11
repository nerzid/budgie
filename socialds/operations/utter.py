from socialds.operations.operation import Operation


class Utter(Operation):
    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs):
        super().execute(*args, **kwargs)
        msg = kwargs['message']
        print(msg)

