from socialds.object import Object


class Info(Object):
    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def __repr__(self):
        return self.name
