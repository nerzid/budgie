import queue

from socialds.other.event_listener import EventListener


class MessageStreamer:

    def __init__(self, messages=None):
        if messages is None:
            messages = queue.Queue()
        self.messages = messages
        self.is_streaming = False
        self.on_message_added = EventListener()

    def add(self, message):
        # print('message added ' + str(message))
        self.messages.put(item=message, block=True)
        # self.messages.put_nowait(message)
        # print(self.messages.)
        self.on_message_added.invoke()

    def stream(self):
        yield self.messages.get(block=True)
