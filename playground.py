from socialds.agent import Agent
from socialds.any.any_agent import AnyAgent
from socialds.any.any_place import AnyPlace
from socialds.dialogue_system import DialogueSystem
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.place import Place
from socialds.states.relation import Relation
from socialds.utterance import Utterance

# Global properties
any_place = AnyPlace()
places_office = Place('office')
place_waiting_room = Place('waiting room')

any_agent = AnyAgent()
# Agent 1: Joe - patient
# Agent 1's Relation Storages
agent1_kb = RelationStorage('Knowledgebase')
agent1_competences = RelationStorage('Competences')
agent1_places = RelationStorage('Places')
agent1_resources = RelationStorage('Resources')
agent1_forgotten = RelationStorage('Forgotten Knowledgebase')
actor1 = Actor(name="Actor1", knowledgebase=RelationStorage('Actor\'s Knowledgebase'))

# Agent 1's initialization
agent1 = Agent(name='First Agent', actor=actor1, roles=[], knowledgebase=agent1_kb, forgotten=agent1_forgotten,
               competences=agent1_competences, places=agent1_places, resources=agent1_resources)


# Agent 2: Jane - doctor
# Agent 2's Relation Storages
agent2_kb = RelationStorage('Knowledgebase')
agent2_forgotten = RelationStorage('Forgotten Knowledgebase')
agent2_competences = RelationStorage('Competences')
agent2_places = RelationStorage('Places')
agent2_resources = RelationStorage('Resources')

# Agent 2's initialization
agent2 = Agent(name='Agent2',
               actor=Actor(name="Actor2", knowledgebase=RelationStorage('Actor\'s Knowledgebase ')),
               forgotten=agent2_forgotten,
               roles=[],
               knowledgebase=agent2_kb, competences=agent2_competences, places=agent2_places,
               resources=agent2_resources)


ds = DialogueSystem(
    agents=[agent1, agent2],
    utterances=[
        Utterance(text='Hi', actions=[]),
        Utterance(text='Yoo', actions=[])
    ],
)
ds.run(4)