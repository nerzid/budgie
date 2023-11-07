from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RelationTense


def op_and():
    pass


def op_then():
    pass


def op_or():
    pass


def add_relation(relation: Relation, rs: RelationStorage):
    rs.add(relation)


def move_relation(relation: Relation, from_rs: RelationStorage, to_rs: RelationStorage):
    from_rs.remove(relation)
    to_rs.add(relation)


def share_relation(relation: Relation, shared_with: RelationStorage):
    shared_with.add(relation)
    

def modify_right(relation: Relation, new_right: any):
    relation.right = new_right
    # I might need to modify the relation storage dict
    

def modify_left(relation: Relation, new_left: any):
    relation.left = new_left
    # modify the relation storage dict as well
    

def modify_tense(relation: Relation, new_tense: RelationTense):
    relation.r_tense = new_tense
    # modify the relation storage dict as well