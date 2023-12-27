from typing import List

from socialds.relationstorage import RelationStorage
from socialds.rs_holder import RSHolder, RSHolderType


class Place(RSHolder):
    def __init__(self, name, resources: RelationStorage = None, places_inside=None):
        RSHolder.__init__(self, rsholder_name=name,
                          rsholder_type=RSHolderType.PLACE)
        if places_inside is None:
            places_inside = []
        self.places_inside = places_inside
        if resources is None:
            self.resources = RelationStorage(f'Resources at {name}')
        else:
            self.resources = resources
        self.name = name

    def __eq__(self, other):
        from socialds.any.any_place import AnyPlace
        if isinstance(other, AnyPlace):
            return True
        else:
            return self.name == other.name and self.resources == other.resources

    def __repr__(self):
        return self.name
