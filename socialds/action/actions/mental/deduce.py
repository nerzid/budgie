from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.states.relation import Relation


class Deduce(Action):
    def __init__(self, deducer: Agent, deduced: Relation):
        """
        Agent thinks and arrives at a certain relation.
        E.g., after thinking, doctor figures out that the patient has bacterial conjunctivitis
        :param deducer: The agent who deduces the relation as fact
        :param deduced: The deduced information as relation to be stored in the deducer's knowledgebase
        """
        self.deducer = deducer
        self.deduced = deduced
        super().__init__('deduce', ActionObjType.MENTAL, [])

    def colorless_repr(self):
        return f"{super().colorless_repr()}({self.deducer.name} deduces that {self.deduced.colorless_repr()})"

    def __repr__(self):
        return f"{super().__repr__()}({self.deducer.name} deduces that {self.deduced})"

    def execute(self):
        self.deducer.knowledgebase.add(self.deduced)
        super().execute()
