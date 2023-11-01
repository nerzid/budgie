from socialds.managers.events.channel import Channel
from socialds.managers.events.event import Event


class EventManager:
    def __init__(self):
        self.channels = self.__build_channels__()

    def receive(self, event: Event):
        print(f'Received event: {event.name}')

    def send(self, event: Event):
        print(f'Sent event: {event.name}')

    def __build_channels__(self):
        channels = list()
        for i in range(0, 100):
            channels.append(Channel(cid=i, active=True))
        return channels
