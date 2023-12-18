from socialds.action.action import Action
from socialds.action.action_obj import ActionObjType
from socialds.any.any_agent import AnyAgent
from socialds.any.any_object import AnyObject


class AnyAction(Action, AnyObject):
    def __init__(self):
        super().__init__('any action', AnyAgent(), ActionObjType.ANY, [])

    def __repr__(self):
        return 'any-action'
