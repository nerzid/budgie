import uuid


class Value:
    def __init__(self, name: str, amount: float = 0, max_amount: float = 100):
        self.id = str(uuid.uuid4())
        self.name = name
        self.amount = amount
        self.max_amount = max_amount

    def __repr__(self):
        return self.name
