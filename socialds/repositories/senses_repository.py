from socialds.senses.sense import Sense, SenseVariation
from socialds.repositories.action_repository import verbal_greet, op_and, physical_wave


def greeting_a_person():
    return Sense(desc="greeting a person", variations=[
        SenseVariation(desc="greeting by talking only",
                       action_seq=[
                           verbal_greet(),
                           op_and(),
                           physical_wave()
                       ])
    ])
