from socialds.conditions.condition import Condition
from socialds.message import Message


class Goal:
    def __init__(self, owner, name: str, conditions: [Condition], desc: str = ''):
        self.name = name
        self.desc = desc
        self.conditions = conditions
        self.owner = owner
        self.is_reached_first_time = False

    def is_reached(self, checker):
        """
        Checks if the goal is reached
        :return: True if all the conditions yield true
        """
        reached = True
        for condition in self.conditions:
            # print(condition)
            reached = reached and condition.check(checker)
        if not self.is_reached_first_time and reached:
            self.is_reached_first_time = True
            from socialds.enums import DSAction
            from socialds.enums import DSActionByType
            checker.message_streamer.add(Message(ds_action=DSAction.DISPLAY_LOG.value,
                                                 ds_action_by='Dialogue System',
                                                 ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                                 message='Goal {} is reached!'.format(self.name)))
        return reached

    def __str__(self):
        return f'Goal: {self.name}\n' \
               f'Desc: {self.desc}\n' \
               f'Conditions: {self.conditions}'
