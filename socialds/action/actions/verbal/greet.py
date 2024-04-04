from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction
from socialds.other.dst_pronouns import DSTPronoun


class Greet(SimpleAction):
    @staticmethod
    def get_class_attr_mapping():
        from socialds.agent import Agent
        attrs = SimpleAction.get_class_attr_mapping()
        attrs.update({
            "Name": "Greet",
            "Done By": [Agent, DSTPronoun],
            "Recipients": [Agent, DSTPronoun]
        })
        return attrs

    def __init__(self):
        super().__init__('greet', done_by=DSTPronoun.I, act_type=ActionObjType.VERBAL, recipient=DSTPronoun.YOU)

    @staticmethod
    def get_pretty_template():
        return "[Done By] greets [Recipients]"

    def __str__(self):
        return "%s %s %s" % (self.done_by, self.name, self.recipient)

    # def __repr__(self):
    #     return "%r %s %r" % (self.done_by, self.name, self.recipient)
