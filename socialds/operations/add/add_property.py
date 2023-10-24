from object import Object
from operations.stateoperation import StateOperation
from states.property import Property


class AddProperty(StateOperation):
    def __init__(self, obj: Object, prop: Property):
        super().__init__()
        self.obj = obj
        self.prop = prop

    def execute(self):
        self.obj.properties.add(self.prop)