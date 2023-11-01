from socialds.agent import Agent
from socialds.dialogue_system import DialogueSystem
from socialds.repositories.action_repository import verbal_greet, op_and, physical_wave
from socialds.utterance import Utterance
from socialds.socialpractice.context.actor import Actor

utts = [
    Utterance(text="Hi", actions=[verbal_greet()]),
    Utterance(text="Hey!", actions=[verbal_greet()])
]

agent1 = Agent(actor=Actor(name="Eren", competences=[]), roles=[])
agent2 = Agent(actor=Actor(name="Wika", competences=[]), roles=[])

ds = DialogueSystem(agents=[agent1, agent2], utterances=utts)
ds.run(turns=2)
