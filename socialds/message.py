from socialds.enums import DSAction, DSActionByType


class Message:
    def __init__(self, ds_action: DSAction, ds_action_by, ds_action_by_type: DSActionByType, message: any, **kwargs):
        self.ds_action = ds_action
        self.ds_action_by = ds_action_by
        self.ds_action_by_type = ds_action_by_type
        self.message = message
        self.message_obj = None
        self.make(**kwargs)

    def __str__(self):
        return self.message_obj

    def make(self, **kwargs):
        self.message_obj = {'ds_action_by_type': self.ds_action_by_type,
                            'ds_action_by': self.ds_action_by,
                            'message': self.message,
                            'ds_action': self.ds_action}
        for k, v in kwargs.items():
            self.message_obj.update({k: v})
