from __future__ import annotations

from socialds.action.action_time import ActionHappenedAtTime
from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.agent import Agent
from socialds.other.dst_pronouns import DSTPronoun, pronouns
from socialds.states.property import Property


class Have(Action):
    def __init__(self, done_by: Agent | DSTPronoun, target: Property, times: [ActionHappenedAtTime] = None):
        self.target = target
        super().__init__('has', done_by, ActionObjType.PHYSICAL, [], times=times)

    def __str__(self):
        return "%s has %s %s" % (self.done_by, self.target, self.get_times_str())

    def __repr__(self):
        return "%r has %r %r" % (self.done_by, self.target, self.get_times_str())
    
    def insert_pronouns(self):
        super().insert_pronouns()
    
    def execute(self):
        self.insert_pronouns()
        super().execute()
