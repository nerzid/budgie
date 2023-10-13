from object import Object
from stateoperations.stateoperation import StateOperation
from states.property import Property


class DeleteProperty(StateOperation):
    def __init__(self, obj: Object, prop: Property):
        super().__init__()
        self.obj = obj
        self.prop = prop

    def execute(self):
        self.obj.properties.remove(self.prop)