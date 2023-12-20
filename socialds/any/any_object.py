class AnyObject:
    def __repr__(self):
        return 'any-object'

    def __eq__(self, other):
        from socialds.object import Object
        if isinstance(other, Object):
            return True
        return False
