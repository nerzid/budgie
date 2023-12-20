from enum import Enum
from typing import Dict

from socialds.relationstorage import RelationStorage, RSType


class RSHolderType(Enum):
    AGENT = 'agent'
    RESOURCE = 'resource'


class RSHolder:
    def __init__(self, rsholder_name: str, rsholder_type: RSHolderType = RSHolderType.RESOURCE,
                 relation_storages: Dict[RSType, RelationStorage] = None):
        self.rsholder_type = rsholder_type
        self.relation_storages = relation_storages
        self.rsholder_name = rsholder_name
        if self.relation_storages is None:
            if rsholder_type is RSHolderType.AGENT:
                self.relation_storages = {
                    RSType.KNOWLEDGEBASE: RelationStorage(rsholder_name + ' Knowledgebase'),
                    RSType.FORGOTTEN: RelationStorage(rsholder_name + ' Forgotten'),
                    RSType.COMPETENCES: RelationStorage(rsholder_name + ' Competences'),
                    RSType.RESOURCES: RelationStorage(rsholder_name + ' Resources'),
                    RSType.PLACES: RelationStorage(rsholder_name + ' Places'),
                    RSType.EXPECTED_ACTIONS: RelationStorage(rsholder_name + ' Expected Actions'),
                    RSType.EXPECTED_EFFECTS: RelationStorage(rsholder_name + ' Expected Effects'),
                    RSType.VALUES: RelationStorage(rsholder_name + ' Values'),
                }
            elif rsholder_type is RSHolderType.RESOURCE:
                self.relation_storages = {
                    RSType.PROPERTIES: RelationStorage(rsholder_name + ' Properties'),
                    RSType.PLACES: RelationStorage(rsholder_name + ' Places')
                }
