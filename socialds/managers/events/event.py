from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def do(self):
        pass
