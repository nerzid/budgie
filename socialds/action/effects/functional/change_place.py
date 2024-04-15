from __future__ import annotations

from abc import abstractmethod
from typing import List

from socialds.action.effects.effect import Effect
import socialds.conditions.object_at_place as oap
from socialds.enums import Tense
from socialds.operations.add_relation_to_rsholder import AddRelationToRSHolder
from socialds.operations.find_one_relation_in_rsholder import FindOneRelationInRSHolder
from socialds.operations.modify_relation_tense import ModifyRelationTense
from socialds.other.dst_pronouns import DSTPronoun
from socialds.relationstorage import RSType
from socialds.socialpractice.context.place import Place
from socialds.states.relation import RType, Relation, Negation


class ChangePlace(Effect):
    def __init__(self, from_place: Place, to_place: Place, affected: 'Agent' | DSTPronoun):
        self.from_place = from_place
        self.to_place = to_place
        op_seq = [
            ModifyRelationTense(
                relation=FindOneRelationInRSHolder(
                    rsholder=affected,
                    rstype=RSType.PLACES,
                    left=affected,
                    rtype=RType.IS_AT,
                    rtense=Tense.PRESENT,
                    right=from_place,
                    negation=Negation.FALSE
                ), rtense=Tense.PAST),
            AddRelationToRSHolder(
                relation=Relation(left=affected, rtype=RType.IS_AT, rtense=Tense.PRESENT, right=to_place), rsholder=affected, rstype=RSType.PLACES)
        ]
        super().__init__(name='change-location',
                         from_state=[
                             oap.ObjectAtPlace(rsholder=affected,
                                               place=from_place,
                                               tense=Tense.PRESENT,
                                               times=[],
                                               negation=False)
                         ],
                         to_state=[
                             oap.ObjectAtPlace(rsholder=affected,
                                               place=from_place,
                                               tense=Tense.PRESENT,
                                               times=[],
                                               negation=True)
                         ],
                         affected=affected,
                         op_seq=op_seq)

    def __repr__(self):
        return f'Change the place of {self.affected} from {self.from_place} to {self.to_place}'

    @staticmethod
    def get_pretty_template():
        return "Place of [affected] changes from [from_place] to [to_place]"

    @abstractmethod
    def get_requirement_holders(self) -> List:
        return [self.from_place, self.to_place, self.affected]
