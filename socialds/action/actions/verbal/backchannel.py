from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Backchannel(SimpleAction):
    def __init__(self):
        super().__init__('backchannel', DSTPronoun.I, ActionObjType.VERBAL)

    def __str__(self):
        return "%s %s" % (self.done_by, self.name)

    def __repr__(self):
        return "%r %r" % (self.done_by, self.name)
