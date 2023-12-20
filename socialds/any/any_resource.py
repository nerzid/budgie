from socialds.any.any_object import AnyObject
from socialds.socialpractice.context.resource import Resource


class AnyResource(Resource, AnyObject):
    def __init__(self):
        super().__init__('any resource')

    def __eq__(self, other):
        if isinstance(other, Resource):
            return True
        return False
