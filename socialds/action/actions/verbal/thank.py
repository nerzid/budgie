from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Thank(SimpleAction):

    @staticmethod
    def get_class_attr_mapping():
        from socialds.agent import Agent
        return super().get_class_attr_mapping().update({
            "Name": "Thank",
            "Done By": [Agent, DSTPronoun],
            "Recipients": [Agent, DSTPronoun]
        })

    def __init__(self):
        super().__init__('thank', DSTPronoun.I, ActionObjType.VERBAL, recipient=DSTPronoun.YOU)

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    def __repr__(self):
        return "%r %r %r" % (self.done_by, self.name, self.recipient)
