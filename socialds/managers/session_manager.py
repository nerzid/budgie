import textwrap
from typing import List

from termcolor import colored

from socialds.conditions.condition import Condition
from socialds.enums import TermColor, DSAction, DSActionByType
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
    def update_expectations(agent):
        for expectation in vars.expectations:
            expectation.update_status(agent)

    @staticmethod
    def update_session_statuses(agent):
        from socialds.managers.managers import message_streamer
        for session in vars.sessions:
            # No need to update the status of session if it is already completed or failed
            if session.status == SessionStatus.COMPLETED or session.status == SessionStatus.FAILED:
                continue

            is_start_conditions_true = Condition.check_conditions(session.start_conditions, agent)
            is_end_conditions_true = True
            for goal in session.end_goals:
                is_end_conditions_true = is_end_conditions_true and goal.is_reached(agent)
            if session.status == SessionStatus.NOT_STARTED:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                    message_streamer.add(ds_action=DSAction.DISPLAY_LOG.value,
                                         ds_action_by='Dialogue System',
                                         ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                         message='The session {} is completed without even being started'.format(session.name))
                elif is_start_conditions_true:
                    session.status = SessionStatus.ONGOING
                    message_streamer.add(ds_action=DSAction.DISPLAY_LOG.value,
                                         ds_action_by='Dialogue System',
                                         ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                         message='The session {} is started and ongoing now.'.format(session.name))
            elif session.status == SessionStatus.ONGOING:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                    message_streamer.add(ds_action=DSAction.DISPLAY_LOG.value,
                                         ds_action_by='Dialogue System',
                                         ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                                         message='The session {} is completed!'.format(session.name))

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
    def get_sessions_info(agent):
        info = ''
        for session in vars.sessions:
            info += session.name + '\n'
            info += 'Start Conditions' + '\n'
            for condition in session.start_conditions:
                condition_str = ('Not Satisfied', 'Satisfied')[condition.check(agent)]
                condition_str += ' -> '
                condition_str += str(condition) + '\n'
                info += condition_str

            info += 'End Conditions' + '\n'
            for goal in session.end_goals:
                for condition in goal.conditions:
                    condition_str = ('Not Satisfied', 'Satisfied')[condition.check(agent)]
                    condition_str += ' -> '
                    condition_str += str(condition) + '\n'
                    info += condition_str
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
                condition_str = ('Not Satisfied', 'Satisfied')[condition.check()]
                condition_str += ' -> '
                condition_str += str(condition) + '\n'
                info += textwrap.indent(text=condition_str, prefix='  ')

            info += colored(text='Expectations\n', color=TermColor.LIGHT_MAGENTA.value)
            for expectation in session.expectations:
                # info += ('Not Satisfied', 'Satisfied')[condition.check()]
                # info += ' -> '
                info += textwrap.indent(text=str(expectation), prefix="  ")

            info += colored(text='End Goals\n', color=TermColor.LIGHT_MAGENTA.value)
            for goal in session.end_goals:
                info += textwrap.indent(text="Goal: %s\n" % goal.name, prefix='  ')
                if goal.desc != '':
                    info += textwrap.indent(text="Desc: %s\n" % goal.desc, prefix='    ')
                info += textwrap.indent(text='Conditions:\n', prefix='    ')
                for condition in goal.conditions:
                    condition_str = ('Not Satisfied', 'Satisfied')[condition.check()]
                    condition_str += ' -> '
                    condition_str += str(condition) + '\n'
                    info += textwrap.indent(text=condition_str, prefix='      ')
            info += '\n'
        return info
