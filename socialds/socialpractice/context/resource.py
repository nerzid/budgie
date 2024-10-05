import uuid
from socialds.object import Object
from socialds.relationstorage import RelationStorage, RSType
from socialds.rs_holder import RSHolder, RSHolderType


class Resource(Object, RSHolder):
    def __init__(self, name, relation_storages: dict = None):
        Object.__init__(self, name)
        RSHolder.__init__(
            self,
            rsholder_name=name,
            rsholder_type=RSHolderType.RESOURCE,
            relation_storages=relation_storages,
        )
        self.name = name

    def __eq__(self, other):
        from socialds.any.any_object import AnyObject

        if isinstance(other, AnyObject):
            return True
        if isinstance(other, Resource):
            return self.name == other.name  # TODO needs more strict equality check here
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
        }
