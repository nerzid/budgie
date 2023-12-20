from typing import List

from termcolor import colored

from socialds.conditions.condition import Condition
from socialds.enums import TermColor
from socialds.exceptions.no_ongoing_session_found_error import NoOngoingSessionFoundError
from socialds.goal import Goal
from socialds.session import Session, SessionStatus
import socialds.other.variables as vars


class SessionManager:
    def __init__(self, sessions: List[Session] = None):
        if sessions is None:
            sessions = []
        vars.sessions = sessions

    @staticmethod
    def add_session(session: Session):
        vars.sessions.append(session)

    @staticmethod
    def add_multi_sessions(sessions: List[Session]):
        for session in sessions:
            SessionManager.add_session(session)

    @staticmethod
    def get_ongoing_session():
        for session in vars.sessions:
            if session.status == SessionStatus.ONGOING:
                return session
        raise NoOngoingSessionFoundError

    @staticmethod
    def get_all_ongoing_sessions() -> List[Session]:
        ongoing_sessions = []
        for session in vars.sessions:
            if session.status == SessionStatus.ONGOING:
                ongoing_sessions.append(session)
        if len(ongoing_sessions) == 0:
            raise NoOngoingSessionFoundError
        else:
            return ongoing_sessions

    @staticmethod
    def update_session_statuses():
        for session in vars.sessions:
            # No need to update the status of session if it is already completed or failed
            if session.status == SessionStatus.COMPLETED or session.status == SessionStatus.FAILED:
                continue

            is_start_conditions_true = Condition.check_conditions(session.start_conditions)
            is_end_conditions_true = True
            for goal in session.end_goals:
                is_end_conditions_true = is_end_conditions_true and goal.is_reached()
            if session.status == SessionStatus.NOT_STARTED:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                elif is_start_conditions_true:
                    session.status = SessionStatus.ONGOING
            elif session.status == SessionStatus.ONGOING:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED

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

    @staticmethod
    def get_sessions_info():
        info = ''
        for session in vars.sessions:
            info += session.name + '\n'
            info += 'Start Conditions' + '\n'
            for condition in session.start_conditions:
                info += str(condition) + '\n'

            info += 'End Conditions' + '\n'
            for condition in session.end_goals:
                info += str(condition) + '\n'
        return info

    @staticmethod
    def get_colorful_sessions_info():
        info = colored('Sessions\n', on_color=TermColor.ON_MAGENTA.value)
        for session in vars.sessions:
            info += colored(text=session.name, on_color=TermColor.ON_LIGHT_MAGENTA.value)
            info += colored(text=session.status.value, on_color=TermColor.ON_WHITE.value,
                            color=TermColor.BLACK.value)
            info += '\n'
            info += colored(text='Start Conditions\n', color=TermColor.LIGHT_MAGENTA.value)
            for condition in session.start_conditions:
                info += ('Not Satisfied', 'Satisfied')[condition.check()]
                info += ' -> '
                info += str(condition) + '\n'

            info += colored(text='Expectations\n', color=TermColor.LIGHT_MAGENTA.value)
            for expectation in session.expectations:
                # info += ('Not Satisfied', 'Satisfied')[condition.check()]
                # info += ' -> '
                info += str(expectation)

            info += colored(text='End Goals\n', color=TermColor.LIGHT_MAGENTA.value)
            for goal in session.end_goals:
                info += f'Goal: {goal.name}\n'
                if goal.desc is not '':
                    info += f'Desc: {goal.desc}\n'
                info += f'Conditions:\n'
                for condition in goal.conditions:
                    info += ('Not Satisfied', 'Satisfied')[condition.check()]
                    info += ' -> '
                    info += str(condition) + '\n'
            info += '\n'
        return info
