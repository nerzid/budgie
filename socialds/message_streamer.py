import queue

from socialds.other.event_listener import EventListener


class MessageStreamer:

    def __init__(self, messages=None):
        if messages is None:
            messages = queue.Queue()
        self.messages = messages
        self.on_message_added = EventListener()

    def add(self, ds_action_by_type, ds_action_by, message, ds_action, **kwargs):
        message = {'ds_action_by_type': ds_action_by_type,
                   'ds_action_by': ds_action_by,
                   'message': message,
                   'ds_action': ds_action}
        for k, v in kwargs.items():
            message.update({k: v})
        self.messages.put(message)
        self.on_message_added.invoke()

    def stream(self):
        yield self.messages.get_nowait()
