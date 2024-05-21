class Emotion:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, value: object) -> bool:
        return self.name == value.name
