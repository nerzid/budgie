from typing import List
import uuid

from socialds.other.unique_id_generator import get_unique_id
from socialds.relationstorage import RelationStorage
from socialds.rs_holder import RSHolder, RSHolderType


class Place(RSHolder):
    def __init__(self, name, resources: RelationStorage = None, places_inside=None):
        RSHolder.__init__(self, rsholder_name=name, rsholder_type=RSHolderType.PLACE)
        if places_inside is None:
            places_inside = []
        self.places_inside = places_inside
        if resources is None:
            self.resources = RelationStorage(f"Resources at {name}")
        else:
            self.resources = resources
        self.name = name
        self.id = get_unique_id()

    def __eq__(self, other):
        from socialds.any.any_place import AnyPlace

        # print('this: {}, other: {}'.format(self, other))
        if isinstance(other, AnyPlace):
            return True
        else:
            return self.name == other.name and self.resources == other.resources

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "resources": [resource.to_dict_with_status() for resource in self.resources]
        }
