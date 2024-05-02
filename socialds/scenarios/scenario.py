from typing import List, Type
import uuid

from socialds.action.action import Action
from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.managers.session_manager import SessionManager
from socialds.relationstorage import RelationStorage
from socialds.socialpractice.context.place import Place
from socialds.socialpractice.context.resource import Resource
from socialds.states.property import Property
from socialds.states.value import Value
from socialds.utterance import Utterance


class Scenario:
    def __init__(
        self,
        name: str,
        agents: List[Agent],
        utterances: List[Utterance],
        actions: List[Type[Action]],
        effects: List[Type[Effect]],
        places: List[Place],
        properties: List[Property],
        resources: List[Resource],
        values: List[Value],
    ) -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.agents = agents
        self.utterances = utterances
        self.actions = actions
        self.effects = effects
        self.places = places
        self.properties = properties
        self.resources = resources
        self.values = values
