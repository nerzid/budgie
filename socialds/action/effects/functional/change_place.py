from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.conditions.agent_at_place import AgentAtPlace
from socialds.conditions.object_at_place import ObjectAtPlace
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.operations.find_one_relation_in_resource import FindOneRelationInResource
from socialds.operations.find_one_relation_in_rsholder import FindOneRelationInRSHolder
from socialds.operations.modify_relation_tense import ModifyRelationTense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.resource import Resource
from socialds.states.relation import RType, Relation


class ChangeLocation(Effect):
    def __init__(self, from_place: any, to_place: any, affected: any):
        op_seq = [
            ModifyRelationTense(
                relation=FindOneRelationInRSHolder(
                    rsholder=affected,
                    rstype=RSType.PLACES,
                    left=affected,
                    rtype=RType.IS_AT,
                    rtense=Tense.PRESENT,
                    right=from_place,
                    negation=False
                ), rtense=Tense.PAST),
            AddRelationToRSHolder(
                relation=Relation(
                    left=affected,
                    rtype=RType.IS_AT,
                    rtense=Tense.PRESENT,
                    right=to_place,
                    negation=False
                ), rsholder=affected, rstype=RSType.PLACES)
        ]
        super().__init__(name='change-location',
                         from_state=[
                             ObjectAtPlace(rsholder=affected,
                                           place=from_place,
                                           tense=Tense.PRESENT,
                                           times=[],
                                           negation=False)
                         ],
                         to_state=[
                             ObjectAtPlace(rsholder=affected,
                                           place=from_place,
                                           tense=Tense.PRESENT,
                                           times=[],
                                           negation=True)
                         ],
                         affected=affected,
                         op_seq=op_seq)
