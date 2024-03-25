from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Bye(SimpleAction):
    def __init__(self):
        super().__init__('bye', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, recipient=DSTPronoun.YOU)

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    # def __repr__(self):
    #     return "%r %s %r" % (self.done_by, self.name, self.recipient)
