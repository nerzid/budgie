from typing import List, Type
import uuid

from socialds.action.action import Action
from socialds.action.effects.effect import Effect
from socialds.agent import Agent
from socialds.managers.session_manager import SessionManager
from socialds.other.unique_id_generator import get_unique_id
from socialds.relationstorage import RelationStorage
from socialds.session import Session
from socialds.socialpractice.context.information import Information
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
            sessions: List[Session],
            actions: List[Type[Action]],
            effects: List[Type[Effect]],
            places: List[Place],
            properties: List[Property],
            resources: List[Resource],
            values: List[Value],
    ) -> None:
        self.id = get_unique_id()
        self.name = name
        self.agents = agents
        self.utterances = utterances
        self.sessions = sessions
        self.actions = actions
        self.effects = effects
        self.places = places
        self.properties = properties
        self.resources = resources
        self.values = values

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "agents": [agent.to_dict() for agent in self.agents],
            "utterances": [utterance.to_dict() for utterance in self.utterances],
            "sessions": [session.to_dict() for session in self.sessions],
            "actions": [action.__name__ for action in self.actions],
            "effects": [effect.__name__ for effect in self.effects],
            "places": [place.to_dict() for place in self.places],
            "properties": [property_.to_dict() for property_ in self.properties],
            "resources": [resource.to_dict() for resource in self.resources],
            "values": [value.to_dict() for value in self.values],
        }

    def get_scenario_object_by_id(self):
        return None
