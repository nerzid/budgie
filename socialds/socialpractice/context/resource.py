from object import Object


class Resource(Object):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
