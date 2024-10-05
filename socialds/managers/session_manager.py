import textwrap
from typing import List

from termcolor import colored

from socialds.conditions.condition import Condition
from socialds.enums import TermColor, DSAction, DSActionByType
from socialds.exceptions.no_ongoing_session_found_error import (
    NoOngoingSessionFoundError,
)
from socialds.goal import Goal
from socialds.message import Message
from socialds.message_streamer import MessageStreamer
from socialds.session import Session, SessionStatus


class SessionManager:
    def __init__(self, sessions: List[Session] = None):
        if sessions is None:
            sessions = []
        self.sessions = sessions
        self.message_streamer: MessageStreamer = None  # type: ignore

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

    def get_all_ongoing_sessions(self) -> List[Session]:
        ongoing_sessions = []
        for session in self.sessions:
            if session.status == SessionStatus.ONGOING:
                ongoing_sessions.append(session)
        if len(ongoing_sessions) == 0:
            raise NoOngoingSessionFoundError
        else:
            return ongoing_sessions

    def update_expectations(self, agent):
        try:
            ongoing_sessions = self.get_all_ongoing_sessions()
        except NoOngoingSessionFoundError:
            print("No ongoing session found. Won't update the expectations")
        else:
            for session in ongoing_sessions:
                for expectation in session.expectations:
                    expectation.update_status(agent)

    def update_session_statuses(self, agent):
        self.update_expectations(agent)
        for session in self.sessions:
            # No need to update the status of session if it is already completed or failed
            if (
                session.status == SessionStatus.COMPLETED
                or session.status == SessionStatus.FAILED
            ):
                continue

            is_start_conditions_true = Condition.check_conditions(
                session.start_conditions, agent
            )
            is_end_conditions_true = True
            for goal in session.end_goals:
                is_end_conditions_true = is_end_conditions_true and goal.is_reached(
                    agent
                )
            if session.status == SessionStatus.NOT_STARTED:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                    self.message_streamer.add(
                        Message(
                            ds_action=DSAction.DISPLAY_LOG.value,
                            ds_action_by="Dialogue System",
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            message="The session {} is completed without even being started".format(
                                session.name
                            ),
                        )
                    )
                elif is_start_conditions_true:
                    session.status = SessionStatus.ONGOING
                    self.message_streamer.add(
                        Message(
                            ds_action=DSAction.DISPLAY_LOG.value,
                            ds_action_by="Dialogue System",
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            message="The session {} is started and ongoing now.".format(
                                session.name
                            ),
                        )
                    )
            elif session.status == SessionStatus.ONGOING:
                if is_end_conditions_true:
                    session.status = SessionStatus.COMPLETED
                    self.message_streamer.add(
                        Message(
                            ds_action=DSAction.DISPLAY_LOG.value,
                            ds_action_by="Dialogue System",
                            ds_action_by_type=DSActionByType.DIALOGUE_SYSTEM.value,
                            message="The session {} is completed!".format(session.name),
                        )
                    )

    def get_sessions_info_dict(self):
        from socialds.any.any_agent import AnyAgent

        agent = AnyAgent()
        result = []
        for session in self.sessions:
            result.append(session.to_dict_with_status(agent))
        return result

    def get_sessions_info(self, agent):
        info = ""
        for session in self.sessions:
            info += session.name + "\n"
            info += "Start Conditions" + "\n"
            for condition in session.start_conditions:
                condition_str = ("Not Satisfied", "Satisfied")[condition.check(agent)]
                condition_str += " -> "
                condition_str += str(condition) + "\n"
                info += condition_str

            info += "End Conditions" + "\n"
            for goal in session.end_goals:
                for condition in goal.conditions:
                    condition_str = ("Not Satisfied", "Satisfied")[
                        condition.check(agent)
                    ]
                    condition_str += " -> "
                    condition_str += str(condition) + "\n"
                    info += condition_str
        return info

    def get_colorful_sessions_info(self):
        info = colored("Sessions\n", on_color=TermColor.ON_MAGENTA.value)
        for session in self.sessions:
            info += colored(
                text=session.name, on_color=TermColor.ON_LIGHT_MAGENTA.value
            )
            info += colored(
                text=session.status.value,
                on_color=TermColor.ON_WHITE.value,
                color=TermColor.BLACK.value,
            )
            info += "\n"
            info += colored(
                text="Start Conditions\n", color=TermColor.LIGHT_MAGENTA.value
            )
            for condition in session.start_conditions:
                condition_str = ("Not Satisfied", "Satisfied")[condition.check()]
                condition_str += " -> "
                condition_str += str(condition) + "\n"
                info += textwrap.indent(text=condition_str, prefix="  ")

            info += colored(text="Expectations\n", color=TermColor.LIGHT_MAGENTA.value)
            for expectation in session.expectations:
                # info += ('Not Satisfied', 'Satisfied')[condition.check()]
                # info += ' -> '
                info += textwrap.indent(text=str(expectation), prefix="  ")

            info += colored(text="End Goals\n", color=TermColor.LIGHT_MAGENTA.value)
            for goal in session.end_goals:
                info += textwrap.indent(text="Goal: %s\n" % goal.name, prefix="  ")
                if goal.desc != "":
                    info += textwrap.indent(
                        text="Desc: %s\n" % goal.desc, prefix="    "
                    )
                info += textwrap.indent(text="Conditions:\n", prefix="    ")
                for condition in goal.conditions:
                    condition_str = ("Not Satisfied", "Satisfied")[condition.check()]
                    condition_str += " -> "
                    condition_str += str(condition) + "\n"
                    info += textwrap.indent(text=condition_str, prefix="      ")
            info += "\n"
        return info
