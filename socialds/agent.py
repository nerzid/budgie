import uuid
from typing import List, Dict

from socialds.dialogue_system import DialogueSystem
from socialds.managers.planner import Planner
from socialds.object import Object
from socialds.relationstorage import RelationStorage, RSType
from socialds.relationstorage import merge_relation_storages
from socialds.rs_holder import RSHolder, RSHolderType
from socialds.socialpractice.context.actor import Actor
from socialds.socialpractice.context.role import Role


class Agent(Object, RSHolder):
    def __init__(self, name: str, actor: Actor, roles: List[Role],
                 relation_storages: Dict[RSType, RelationStorage] = None, auto: bool = False, agent_id=None):
        Object.__init__(self, name=name)
        RSHolder.__init__(self, rsholder_name=name,
                          rsholder_type=RSHolderType.AGENT,
                          relation_storages=relation_storages)
        self.agent_id = agent_id
        if self.agent_id is None:
            self.agent_id = uuid.uuid4()
        self.actor = actor
        self.roles = roles
        self.planner = Planner(self)
        self.auto = auto
        from socialds.other.dst_pronouns import DSTPronoun
        self.pronouns = {DSTPronoun.I: self,
                         DSTPronoun.YOU: None}
        self.update_competences_from_roles()
        # adds the knowledgebase into the agent's knowledgebase
        self.relation_storages[RSType.KNOWLEDGEBASE].add_from_rs(actor.knowledgebase)
        self.dialogue_system = DialogueSystem(self)
        self.message_streamer = None
        self.session_manager = None
        self.utterances_manager = None

    def __eq__(self, other):
        """
        Do not use this method! Therefore, don't use agent in some_agent_list either.
        In order for the pronouns to be inserted correctly, it needs to receiver pronouns
        from outside. Specifically, it should use the pronouns who executes the action/effect
        @param other:
        @return:
        """
        from socialds.other.dst_pronouns import DSTPronoun
        if isinstance(other, Agent):
            return (self.name == other.name
                    and self.actor == other.actor
                    and self.roles == other.roles
                    and self.relation_storages == other.relation_storages
                    and self.auto == other.auto)
        return False

    def equals_with_pronouns(self, other, pronouns):
        from socialds.other.dst_pronouns import DSTPronoun
        if isinstance(self, DSTPronoun):
            _self = pronouns[self]
        else:
            _self = self

        if isinstance(other, DSTPronoun):
            _other = pronouns[other]
        else:
            _other = other

        if isinstance(other, Agent):
            return (_self.name == _other.name
                    and _self.actor == _other.actor
                    and _self.roles == _other.roles
                    and _self.relation_storages == _other.relation_storages
                    and _self.auto == _other.auto)
        return False

    def __repr__(self):
        return "%s" % self.name

    def update_competences_from_roles(self):
        for role in self.roles:
            merge_relation_storages(self.relation_storages[RSType.COMPETENCES], role.competences)

    def info(self):
        pretty_info = ''
        pretty_info += self.name + ' auto=' + str(self.auto) + '\n'
        pretty_info += str(self.relation_storages[RSType.KNOWLEDGEBASE]) + '\n'
        pretty_info += str(self.relation_storages[RSType.COMPETENCES]) + '\n'
        # pretty_info += str(self.actor.knowledgebase) + '\n'
        for role in self.roles:
            pretty_info += role.name + '\n' + role.competences + '\n'
        # # pretty_info += str(self.roles) + '\n'
        # pretty_info += str(self.competences) + '\n'
        # pretty_info += str(self.resources) + '\n'
        pretty_info += str(self.relation_storages[RSType.PLACES])
        pretty_info += str(self.relation_storages[RSType.EXPECTED_ACTIONS])
        pretty_info += str(self.relation_storages[RSType.EXPECTED_EFFECTS])
        pretty_info += str(self.relation_storages[RSType.VALUES])
        return pretty_info

