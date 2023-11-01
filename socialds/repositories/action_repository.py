# from socialds.repositories.repository import Repository
#
#
# class ActionRepository(Repository):
#     def __init__(self):
#         super().__init__()
from socialds.actions.action import Action
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


def verbal_permit():
    pass


def verbal_ask():
    pass


def verbal_thank():
    pass


# Physical acts
def physical_wave():
    pass
