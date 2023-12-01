from socialds.relationstorage import RelationStorage


class Place:
    def __init__(self, name, resources: RelationStorage = None):
        if resources is None:
            self.resources = RelationStorage(f'Resources at {name}')
        else:
            self.resources = resources
        self.name = name

    def __repr__(self):
        return self.name
