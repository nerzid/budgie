import unittest

from socialds.agent import Agent
from socialds.any.any_agent import AnyAgent
from socialds.any.any_place import AnyPlace
from socialds.enums import Tense
from socialds.relationstorage import RelationStorage
from socialds.repositories.operation_repository import add_relation, create_then_add_relation
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.place import Place
from socialds.states.property import Property
from socialds.states.relation import Relation, RType


class TestOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.knowledgebase = RelationStorage('knowledgebase')

        self.agent1_kb = RelationStorage('agent1 knowledgebase')
        self.agent1_forgotten = RelationStorage('agent1 forgotten')
        self.agent1_resources = RelationStorage('agent1 resources')
        self.agent1_places = RelationStorage('agent1 places')
        self.agent1_competences = RelationStorage('agent1 competences')
        self.agent1 = Agent(name='agent1', actor=Actor(name='actor1'),
                            roles=[],
                            knowledgebase=self.agent1_kb,
                            forgotten=self.agent1_forgotten,
                            competences=self.agent1_competences,
                            resources=self.agent1_resources,
                            places=self.agent1_places,
                            auto=True)

        self.agent2_kb = RelationStorage('agent2 knowledgebase')
        self.agent2_forgotten = RelationStorage('agent2 forgotten')
        self.agent2_resources = RelationStorage('agent2 resources')
        self.agent2_places = RelationStorage('agent2 places')
        self.agent2_competences = RelationStorage('agent2 competences')
        self.agent2 = Agent(name='agent2', actor=Actor(name='actor2'),
                            roles=[],
                            knowledgebase=self.agent2_kb,
                            forgotten=self.agent2_forgotten,
                            competences=self.agent2_competences,
                            resources=self.agent2_resources,
                            places=self.agent2_places,
                            auto=True)

        self.any_agent = AnyAgent()
        self.any_place = AnyPlace()

        self.place1 = Place('place1')
        self.place2 = Place('place2')

        self.property1 = Property('property1')
        self.property2 = Property('property2')

    def test_add_relation(self):
        relation = Relation(left=self.agent1, r_type=RType.IS, r_tense=Tense.PRESENT, right=self.property1)
        add_relation(relation, self.knowledgebase)
        self.assertIn(member=relation, container=self.knowledgebase)

    def test_create_then_add_relation(self):
        create_then_add_relation(left=self.agent1, r_type=RType.IS, r_tense=Tense.PRESENT, right=self.property1,
                                 negation=False, rs=self.knowledgebase)
        self.assertTrue(self.knowledgebase.contains(
            relation=Relation(left=self.agent1, r_type=RType.IS, r_tense=Tense.PRESENT, right=self.property1,
                              negation=False)))


if __name__ == '__main__':
    unittest.main()
