# Contains data about the role of the agent, e.g., patient, doctor, husband, etc.
from socialds.socialpractice.activitiy.competence import Competence


class Role:
    def __init__(self, name, competences: list[Competence]):
        self.name = name
        self.competences = competences
