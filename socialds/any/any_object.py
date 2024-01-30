from socialds.object import Object


class AnyObject(Object):
    def __init__(self):
        super().__init__('any-object')

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        from socialds.object import Object
        if isinstance(other, Object):
            return True
        return False
