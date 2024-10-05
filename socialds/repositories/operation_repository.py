from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation, RType
from socialds.enums import Tense

# to be used as other operations in op_seq when the actions are executed.
found_relation: Relation


def add_relation(relation: Relation, rs: RelationStorage):
    rs.add(relation)


def create_then_add_relation(left: any, r_type: RType, r_tense: Tense,
                             right: any, negation: bool, rs: RelationStorage):
    rs.add(Relation(left, r_type, r_tense, right, negation))


def find_relation(left: any, r_type: RType, r_tense: Tense,
                  right: any, negation: bool, rs: RelationStorage):
    return rs.get_one(left, r_type, r_tense, right, negation)


def find_relation_by_place(agent: Agent, r_tense: Tense, place: Place) -> Relation:
    return agent.places.get_one(agent, RType.IS_AT, r_tense, place, False)


def move_relation(relation: Relation, from_rs: RelationStorage, to_rs: RelationStorage):
    from_rs.remove(relation)
    to_rs.add(relation)


# def share_relation(relation: Relation, shared_with: RelationStorage):
#     shared_with.add(relation)


def modify_relation_right(relation: Relation, new_right: any):
    relation.right = new_right


def modify_relation_left(relation: Relation, new_left: any):
    relation.left = new_left


def modify_relation_tense(relation: Relation, new_tense: Tense):
    relation.rel_tense = new_tense


def modify_relation_negation(relation: Relation, new_negation: bool):
    relation.negation = new_negation


if __name__ == '__main__':
    rel = Relation(left="Eren", rel_type=RType.IS, rel_tense=Tense.PRESENT, right="dirty")
    rs = RelationStorage(name='rs')
    rs.add(rel)
    print(rs)
    print('after operation')
    rel.left = 'wika'
    print(rel)
    print(rs)
