from functools import partial

from termcolor import colored

from socialds.enums import TermColor
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation, create_then_add_relation
from socialds.action.action import Action
from socialds.states.relation import Relation, RType
from socialds.enums import Tense


class Permit(Action):
    def __init__(self, permitter: Agent, permitted: Relation, r_tense: Tense, negation: bool,
                 rs: RelationStorage):
        # self.relation = Relation(permitter, RelationType.IS_PERMITTED_TO, r_tense, permitted, negation)
        self.permitter = permitter
        self.permitted = permitted
        self.rs = rs
        # super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
        #                  op_seq=[partial(add_relation, self.relation, rs)])
        super().__init__(name='permit', act_type=ActionObjType.FUNCTIONAL,
                         op_seq=[partial(create_then_add_relation, permitter, RType.IS_PERMITTED_TO, r_tense, permitted, negation, rs)])

    def colorless_repr(self):
        return f"{super().__repr__()}({str(self.permitter.name)} permits {self.permitted.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.permitter} permits {self.permitted})"
