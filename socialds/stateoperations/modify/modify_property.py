from object import Object
from stateoperations.stateoperation import StateOperation
from states.property import Property


class ModifyProperty(StateOperation):
    def __init__(self, obj: Object, old_prop: Property, new_prop: Property):
        super().__init__()
        self.obj = obj
        self.old_prop = old_prop
        self.new_prop = new_prop

    def execute(self):
        self.obj.properties.remove(self.old_prop)
        self.obj.properties.add(self.new_prop)