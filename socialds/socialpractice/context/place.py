from socialds.relationstorage import RelationStorage


class Place:
    def __init__(self, name, resources: RelationStorage = None):
        if resources is None:
            self.resources = RelationStorage(f'Resources at {name}')
        else:
            self.resources = resources
        self.name = name

    def __eq__(self, other):
        from socialds.any.any_place import AnyPlace
        if isinstance(other, AnyPlace):
            return True
        else:
            return self.name == other.name and self.resources == other.resources

    def __repr__(self):
        return self.name
