from socialds.relationstorage import RelationStorage
from socialds.managers.session_manager import SessionManager

session_manager = SessionManager()
dialogue_history = RelationStorage(name='Dialogue History', is_private=False)
