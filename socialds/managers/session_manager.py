from socialds.agent import Agent
from socialds.relationstorage import RelationStorage
from socialds.exceptions.no_ongoing_session_found_error import NoOngoingSessionFoundError
from socialds.session import Session, SessionStatus
from socialds.states.relation import RelationType
from socialpractice.context.place import Place
from states.property import Property


class SessionManager:
    def __init__(self, sessions: [Session], agents: [Agent], history: RelationStorage):
        self.sessions = sessions
        self.agents = agents
        self.history = history

    def get_ongoing_session(self):
        for session in self.sessions:
            if session.status == SessionStatus.ONGOING:
                return session
        raise NoOngoingSessionFoundError

    def update_session_statuses(self):
        for session in self.sessions:
            # No need to update the status of session if it is already completed or failed
            if session.status == SessionStatus.COMPLETED or session.status == SessionStatus.FAILED:
                continue

            is_start_conditions_true = self.check_conditions(session.start_conditions)
            is_end_conditions_true = self.check_conditions(session.end_conditions)
            if session.status == SessionStatus.NOT_STARTED:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                elif is_start_conditions_true:
                    session.status = SessionStatus.ONGOING
            elif session.status == SessionStatus.ONGOING:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED

    def check_conditions(self, conditions):
        """
        Returns true if all conditions are true
        :param conditions:
        """
        is_all_conditions_true = True
        for condition in conditions:
            relation = condition.relation
            if relation.r_type == RelationType.ACTION:
                if relation in self.history and not condition.negation:
                    continue
                elif relation not in self.history and condition.negation:
                    continue
                else:
                    # TODO handle if relation.left is another relation
                    is_all_conditions_true = False
            elif relation.r_type == RelationType.HAS:
                if isinstance(relation.left, Agent) and \
                        relation in relation.left.knowledgebase and not \
                        condition.negation:
                    continue
                elif isinstance(relation.left, Agent) and \
                        relation not in relation.left.knowledgebase and \
                        condition.negation:
                    continue
                else:
                    # TODO handle if relation.left is Property
                    # TODO handle if relation.left is another relation
                    is_all_conditions_true = False
            elif relation.r_type == RelationType.IS_AT:
                if isinstance(relation.left, Agent) and \
                        isinstance(relation.right, Place) and \
                        relation.right in relation.left.places and \
                        not condition.negation:
                    continue
                elif isinstance(relation.left, Agent) and \
                        isinstance(relation.right, Place) and \
                        relation.right not in relation.left.places and \
                        condition.negation:
                    continue
                else:
                    is_all_conditions_true = False
            elif relation.r_type == RelationType.IS:
                pass
            elif relation.r_type == RelationType.CAN:
                pass
            elif relation.r_type == RelationType.IS_PERMITTED_TO:
                pass
        return is_all_conditions_true
