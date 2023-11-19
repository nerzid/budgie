from functools import partial

from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.repositories.operation_repository import add_relation
from socialds.states.relation import Relation


class Learn(Action):

    def __init__(self, learner: Agent, learned: Relation):
        """
        Learns a piece of information as relation. Learn is similar to Share except only agent who does
        the action saves the new information in their knowledgebase.
        :param learner: The agent who learns the new information
        :param learned: Information to be learned and saved in agent's knowledgebase e.g., patient's eye -has-> inflammation
        """
        super().__init__(name="learn", act_type=ActionObjType.FUNCTIONAL,
                         op_seq=[partial(add_relation, learned, learner.knowledgebase)])
        self.learner = learner
        self.learned = learned

    def colorless_repr(self):
        return f"{super().colorless_repr()}{self.learner} learns {self.learned.colorless_repr()}"

    def __repr__(self):
        return f"{super().__repr__()}{self.learner} learns {self.learned}"
