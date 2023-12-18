from socialds.any.any_object import AnyObject
from socialds.socialpractice.context.place import Place


class AnyPlace(Place, AnyObject):
    def __init__(self):
        super().__init__('any-place')
