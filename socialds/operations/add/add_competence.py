from object import Object
from operations.stateoperation import StateOperation
from states.relation import Relation


class AddCompetence(StateOperation):
    def __init__(self, obj: Object, property_name: str, property_value: str):
        super().__init__()
        self.obj = obj
        self.property_name = property_name
        self.property_value = property_value

    def execute(self):
        super().execute()
        self.obj.properties[self.property_name] = self.property_value
