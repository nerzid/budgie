# from socialds.repositories.repository import Repository
#
#
# class ActionRepository(Repository):
#     def __init__(self):
#         super().__init__()
from senses.sense import Sense, SenseVariation


def action_greet():
    sense = Sense(desc="greeting a person", variations=[
        SenseVariation(desc="greeting by hand waving", op_seq=[])
    ])
