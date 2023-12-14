from socialds.object import Object
from socialds.relationstorage import RelationStorage, RSType
from socialds.rs_holder import RSHolder, RSHolderType


class Resource(Object, RSHolder):
    def __init__(self, name, relation_storages: dict = None):
        Object.__init__(self, name)
        RSHolder.__init__(self, rsholder_name=name,
                          rsholder_type=RSHolderType.RESOURCE,
                          relation_storages=relation_storages)
        self.name = name

