class Placeholder:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Placeholder):
            return self.symbol == other.symbol
        return False

    def __hash__(self) -> int:
        return hash(self.symbol)
