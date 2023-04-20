from managers.events.event import Event


class TextEvent(Event):
    def __init__(self, name, text):
        super().__init__(name)
        self.text = text

    def do(self):
        print(self.text)

