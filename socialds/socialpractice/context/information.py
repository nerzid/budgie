from __future__ import annotations

from typing import List

from socialds.action.action_time import ActionHappenedAtTime
from socialds.rs_holder import RSHolder, RSHolderType
from socialds.states.relation import Relation, RType, Tense, Negation


class Information(Relation, RSHolder):
    # def __init__(self, left: Object | "Information" | Agent | DSTPronoun, rtype: RType, rtense: Tense, right: any,
    def __init__(
        self,
        left,
        rel_type: RType,
        rel_tense: Tense,
        right,
        negation: Negation = Negation.FALSE,
        times: List[ActionHappenedAtTime] = None,
    ):
        Relation.__init__(
            self,
            left=left,
            rel_type=rel_type,
            rel_tense=rel_tense,
            right=right,
            negation=negation,
            times=times,
        )
        RSHolder.__init__(
            self, rsholder_name="information", rsholder_type=RSHolderType.INFORMATION
        )

    def __eq__(self, other):
        from socialds.any.any_relation import AnyRelation

        if isinstance(other, AnyRelation):
            return True
        if isinstance(other, Information):
            return (
                self.left == other.left
                and (
                        self.rel_type == other.rel_type
                        or self.rel_type == RType.ANY
                        or other.rel_type == RType.ANY
                )
                and (
                        self.rel_tense == other.rel_tense
                        or self.rel_tense == Tense.ANY
                        or other.rel_tense == Tense.ANY
                )
                and self.negation == other.negation
                and self.right == other.right
                and self.times == other.times
                and self.rsholder_name == other.rsholder_name
            )  # TODO RS check needs to check relations as well
        return False
