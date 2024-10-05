from socialds.any.any_object import AnyObject
from socialds.socialpractice.context.place import Place


class AnyPlace(Place, AnyObject):
    def __init__(self):
        super().__init__('any-place')
        self.id = -3

    def __eq__(self, other):
        if isinstance(other, Place):
            return True
        else:
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
        }
