from functools import partial

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation
from socialds.states.relation import Relation, RelationType, RelationTense


class Share(Action):
    def __init__(self, relation: Relation, rs: RelationStorage):
        super().__init__(name="share", act_type=ActionObjType.FUNCTIONAL, op_seq=[partial(add_relation, relation, rs)])
        self.relation = relation
        self.rs = rs

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.relation.colorless_repr()} is shared with {self.rs.name}"

    def __repr__(self):
        return f"{super().__repr__()}{self.relation} is shared with {self.rs.name}"


if __name__ == '__main__':
    a = Share(
        Relation(left="Eren",
                 r_type=RelationType.IS,
                 r_tense=RelationTense.PRESENT,
                 right='dirty')
        , RelationStorage(name='test kb'))
    print(a)
