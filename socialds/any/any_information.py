from socialds.any.any_agent import AnyAgent
from socialds.any.any_object import AnyObject
from socialds.any.any_property import AnyProperty
from socialds.enums import Tense
from socialds.socialpractice.context.information import Information
from socialds.states.relation import RType


class AnyInformation(Information, AnyObject):
    def __init__(self):
        super().__init__(AnyObject(), RType.ANY, Tense.ANY, AnyProperty())
