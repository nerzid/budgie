class ActionManager:
    def __init__(self):
        self.ongoing_actions = []

    def remove_action(self, action, pronouns):
        index_to_remove = -1
        for i in range(len(self.ongoing_actions)):
            if action.equals_with_pronouns(self.ongoing_actions[i], pronouns):
                index_to_remove = i
                break
        del self.ongoing_actions[index_to_remove]

