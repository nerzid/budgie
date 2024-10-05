from socialds.object import Object


class AnyObject(Object):
    def __init__(self):
        super().__init__('any-object')
        self.id = -5

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        from socialds.object import Object
        if isinstance(other, Object):
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__
        }
