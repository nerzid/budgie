class EventListener:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener_function, *args, **kwargs):
        self.listeners.append((listener_function, args, kwargs))

    def unsubscribe(self, listener_function):
        self.listeners = [(func, args, kwargs) for func, args, kwargs in self.listeners if func != listener_function]

    def invoke(self, *args, **kwargs):
        for listener_function, listener_args, listener_kwargs in self.listeners:
            combined_args = listener_args + args
            combined_kwargs = {**listener_kwargs, **kwargs}
            listener_function(*combined_args, **combined_kwargs)