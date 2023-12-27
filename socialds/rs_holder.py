from enum import Enum
from typing import Dict

import socialds.relationstorage as rs


class RSHolderType(Enum):
    PLACE = 'Place'
    AGENT = 'Agent'
    RESOURCE = 'Resource'


class RSHolder:
    def __init__(self, rsholder_name: str, rsholder_type: RSHolderType = RSHolderType.RESOURCE,
                 relation_storages: Dict[rs.RSType, rs.RelationStorage] = None):
        self.rsholder_type = rsholder_type
        self.relation_storages = relation_storages
        self.rsholder_name = rsholder_name
        if self.relation_storages is None:
            if rsholder_type is RSHolderType.AGENT:
                self.relation_storages = {
                    rs.RSType.KNOWLEDGEBASE: rs.RelationStorage(rsholder_name + ' Knowledgebase'),
                    rs.RSType.FORGOTTEN: rs.RelationStorage(rsholder_name + ' Forgotten'),
                    rs.RSType.COMPETENCES: rs.RelationStorage(rsholder_name + ' Competences'),
                    rs.RSType.PERMITS: rs.RelationStorage(rsholder_name + ' Permits'),
                    rs.RSType.RESOURCES: rs.RelationStorage(rsholder_name + ' Resources'),
                    rs.RSType.PLACES: rs.RelationStorage(rsholder_name + ' Places'),
                    rs.RSType.EXPECTED_ACTIONS: rs.RelationStorage(rsholder_name + ' Expected Actions'),
                    rs.RSType.EXPECTED_EFFECTS: rs.RelationStorage(rsholder_name + ' Expected Effects'),
                    rs.RSType.VALUES: rs.RelationStorage(rsholder_name + ' Values'),
                    rs.RSType.REQUIREMENTS: rs.RelationStorage(rsholder_name + ' Requirements')
                }
            elif rsholder_type is RSHolderType.RESOURCE:
                self.relation_storages = {
                    rs.RSType.PROPERTIES: rs.RelationStorage(rsholder_name + ' Properties'),
                    rs.RSType.PLACES: rs.RelationStorage(rsholder_name + ' Places'),
                    rs.RSType.REQUIREMENTS: rs.RelationStorage(rsholder_name + ' Requirements')
                }
            elif rsholder_type is RSHolderType.PLACE:
                self.relation_storages = {
                    rs.RSType.PROPERTIES: rs.RelationStorage(rsholder_name + ' Properties'),
                    rs.RSType.PLACES: rs.RelationStorage(rsholder_name + ' Places'),
                    rs.RSType.REQUIREMENTS: rs.RelationStorage(rsholder_name + ' Requirements')
                }
