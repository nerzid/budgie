from socialds.action.action_obj import ActionObjType
from socialds.action.simple_action import SimpleAction


class Remember(SimpleAction):
    def __init__(self):
        super().__init__('remember', ActionObjType.MENTAL)
