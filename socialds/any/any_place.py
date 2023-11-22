from socialds.agent import Agent
from socialds.any.any_object import AnyObject
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.place import Place


class AnyPlace(Place, AnyObject):
    def __init__(self):
        super().__init__('any-place')
