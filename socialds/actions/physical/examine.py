from socialds.actions.action_obj import ActionObjType
from socialds.actions.simple_action import SimpleAction


class Examine(SimpleAction):
    def __init__(self):
        super().__init__('examine', ActionObjType.PHYSICAL)