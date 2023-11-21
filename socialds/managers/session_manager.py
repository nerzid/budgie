from typing import List

from termcolor import colored

from socialds.enums import TermColor
from socialds.exceptions.no_ongoing_session_found_error import NoOngoingSessionFoundError
from socialds.session import Session, SessionStatus


class SessionManager:
    def __init__(self, sessions: List[Session] = None):
        if sessions is None:
            sessions = []
        self.sessions = sessions

    def add_session(self, session: Session):
        self.sessions.append(session)

    def add_multi_sessions(self, sessions: List[Session]):
        for session in sessions:
            self.add_session(session)

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
        for condition in conditions:
            if condition.check() is False:
                return False
        return True

    # def check_conditions(self, conditions):
    #     """
    #     Returns true if all conditions are true
    #     :param conditions:
    #     """
    #     is_all_conditions_true = True
    #     for condition in conditions:
    #         relation = condition.relation
    #         if relation.r_type == RelationType.ACTION:
    #             if relation in managers.dialogue_history and not condition.negation:
    #                 continue
    #             elif relation not in managers.dialogue_history and condition.negation:
    #                 continue
    #             else:
    #                 # TODO handle if relation.left is another relation
    #                 is_all_conditions_true = False
    #         elif relation.r_type == RelationType.HAS:
    #             if isinstance(relation.left, Agent) and \
    #                     relation in relation.left.knowledgebase and not \
    #                     condition.negation:
    #                 continue
    #             elif isinstance(relation.left, Agent) and \
    #                     relation not in relation.left.knowledgebase and \
    #                     condition.negation:
    #                 continue
    #             else:
    #                 # TODO handle if relation.left is Property
    #                 # TODO handle if relation.left is another relation
    #                 is_all_conditions_true = False
    #         elif relation.r_type == RelationType.IS_AT:
    #             if isinstance(relation.left, Agent) and \
    #                     isinstance(relation.right, Place) and \
    #                     relation.right in relation.left.places and \
    #                     not condition.negation:
    #                 continue
    #             elif isinstance(relation.left, Agent) and \
    #                     isinstance(relation.right, Place) and \
    #                     relation.right not in relation.left.places and \
    #                     condition.negation:
    #                 continue
    #             else:
    #                 is_all_conditions_true = False
    #         elif relation.r_type == RelationType.IS:
    #             pass
    #         elif relation.r_type == RelationType.CAN:
    #             pass
    #         elif relation.r_type == RelationType.IS_PERMITTED_TO:
    #             pass
    #     return is_all_conditions_true

    def get_sessions_info(self):
        info = ''
        for session in self.sessions:
            info += session.name + '\n'
            info += 'Start Conditions' + '\n'
            for condition in session.start_conditions:
                info += str(condition) + '\n'

            info += 'End Conditions' + '\n'
            for condition in session.end_conditions:
                info += str(condition) + '\n'
        return info

    def get_colorful_sessions_info(self):
        info = colored('Sessions\n', on_color=TermColor.ON_MAGENTA.value)
        for session in self.sessions:
            info += colored(text=session.name, on_color=TermColor.ON_LIGHT_MAGENTA.value)
            info += colored(text=session.status.value + '\n', on_color=TermColor.ON_WHITE.value,
                            color=TermColor.BLACK.value)
            info += colored(text='Start Conditions\n', color=TermColor.LIGHT_MAGENTA.value)
            for condition in session.start_conditions:
                info += str(condition) + '\n'

            info += colored(text='End Conditions\n', color=TermColor.LIGHT_MAGENTA.value)
            for condition in session.end_conditions:
                info += str(condition) + '\n'
        return info
