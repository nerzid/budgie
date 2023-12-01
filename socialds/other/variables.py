from socialds.relationstorage import RelationStorage

# keeps the dialogue history including the actions that were taken and said utterances
dialogue_history = RelationStorage(name='Dialogue History', is_private=False)

# relations that can be used to deduce another relation from
deducibles = RelationStorage(name='Deducibles', is_private=False)

#

# sessions of the social practice. E.g., opening, history-taking, closing, examination, etc.
sessions = []
