import uuid

from socialds.other.unique_id_generator import get_unique_id


class Value:
    def __init__(self, name: str, amount: float = 0, max_amount: float = 100):
        self.id = get_unique_id()
        self.name = name
        self.amount = amount
        self.max_amount = max_amount

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            "type": self.__class__.__name__,
            'amount': self.amount,
            'max_amount': self.max_amount
        }
