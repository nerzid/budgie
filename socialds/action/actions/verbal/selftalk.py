from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun, pronouns


class SelfTalk(SimpleAction):
    def __init__(self):
        super().__init__('self-talk', DSTPronoun.I, ActionObjType.VERBAL)

    def __str__(self):
        return "%s %s" % (self.done_by, self.name)

    def __repr__(self):
        return "%r %r" % (self.done_by, self.name)
