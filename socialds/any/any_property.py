from socialds.agent import Agent
from socialds.any.any_object import AnyObject
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor
from socialds.states.property import Property


class AnyProperty(Property, AnyObject):
    def __init__(self):
        super().__init__('any-property')
        self.id = -1

    def __eq__(self, other):
        if isinstance(other, Property):
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.__class__.__name__,
        }