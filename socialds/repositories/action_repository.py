# from socialds.repositories.repository import Repository
#
#
# class ActionRepository(Repository):
#     def __init__(self):
#         super().__init__()
from socialds.agent import Agent
from socialds.enums import SemanticEvent
from socialds.actions.action import Action
from socialds.socialpractice.context.info import Info
from socialds.states.relation import Relation, RelationTense, RelationType


# from senses.sense import Sense, SenseVariation


# Operators
def op_and():
    pass


def op_then():
    pass


def op_or():
    pass


# Verbal acts
def verbal_greet():
    return Action(name="Verbal:greet", op_seq=[])


def verbal_permit(semantic_roles: dict):
    return Action(name="Functional:permit", op_seq=[])


def share(beneficiary: Agent, info: Relation):
    # use the info, find the correct semantic role
    # create a relation between the receiver agent and the info
    # the relation type should be know
    beneficiary.actor.knowledgebase.add(relation=info)


def verbal_ask():
    pass


def verbal_thank():
    pass


# Physical acts
def physical_wave():
    pass
