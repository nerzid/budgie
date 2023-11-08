from socialds.relationstorage import RelationStorage
from socialds.states.relation import Relation, RelationTense, RelationType


def op_and():
    pass


def op_then():
    pass


def op_or():
    pass


def add_relation(relation: Relation, rs: RelationStorage):
    rs.add(relation)
    

def create_then_add_relation(left:any, right:any, r_type:RelationType, r_tense:RelationTense, negation:bool, rs:RelationStorage):
    rs.add(Relation(left, r_type, r_tense, right, negation))


def move_relation(relation: Relation, from_rs: RelationStorage, to_rs: RelationStorage):
    from_rs.remove(relation)
    to_rs.add(relation)


def share_relation(relation: Relation, shared_with: RelationStorage):
    shared_with.add(relation)
    

def modify_relation_right(relation: Relation, new_right: any):
    relation.right = new_right
    

def modify_relation_left(relation: Relation, new_left: any):
    relation.left = new_left
    

def modify_relation_tense(relation: Relation, new_tense: RelationTense):
    relation.r_tense = new_tense


def modify_relation_negation(relation: Relation, new_negation: bool):
    relation.negation = new_negation


if __name__ == '__main__':
    rel = Relation(left="Eren", r_type=RelationType.IS, r_tense=RelationTense.PRESENT, right="dirty")
    rs = RelationStorage(name='rs')
    rs.add(rel)
    print(rs)
    print('after operation')
    rel.left = 'wika'
    print(rel)
    print(rs)
