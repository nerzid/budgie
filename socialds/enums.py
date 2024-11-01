from enum import Enum


class TermColor(Enum):
    LIGHT_BLUE = "light_blue"
    LIGHT_YELLOW = "light_yellow"
    LIGHT_RED = "light_red"
    LIGHT_GREEN = "light_green"
    LIGHT_CYAN = "light_cyan"
    LIGHT_MAGENTA = "light_magenta"
    RED = "red"
    BLACK = "black"
    GREY = "grey"
    GREEN = "green"
    ON_RED = "on_red"
    ON_CYAN = "on_cyan"
    ON_BLUE = "on_blue"
    ON_WHITE = "on_white"
    ON_GREEN = "on_green"
    ON_MAGENTA = "on_magenta"
    ON_YELLOW = "on_yellow"
    ON_LIGHT_MAGENTA = "on_light_magenta"


class SemanticEvent(Enum):
    AGENT = "agent"
    PARTNER = "partner"
    CAUSE = "cause"
    INSTRUMENT = "instrument"
    PATIENT = "patient"
    THEME = "theme"
    BENEFICIARY = "beneficiary"
    GOAL = "goal"
    SOURCE = "source"
    RESULT = "result"
    REASON = "reason"
    PURPOSE = "purpose"
    MANNER = "manner"
    MEDIUM = "medium"
    MEANS = "means"
    TIME = "time"
    INITIAL_TIME = "initial time"
    FINAL_TIME = "final time"
    DURATION = "duration"
    SETTING = "setting"
    LOCATION = "location"
    INITIAL_LOCATION = "initial location"
    FINAL_LOCATION = "final location"
    DISTANCE = "distance"
    PATH = "path"
    FREQUENCY = "frequency"
    AMOUNT = "amount"


class SemanticState(Enum):
    ATTRIBUTE = "attribute"
    PIVOT = "PIVOT"
    INSTRUMENT = "instrument"
    SETTING = "setting"
    THEME = "theme"
    BENEFICIARY = "beneficiary"
    REASON = "reason"
    TIME = "time"
    INITIAL_TIME = "initial time"
    FINAL_TIME = "final time"
    DURATION = "duration"
    MANNER = "manner"
    LOCATION = "location"
    INITIAL_LOCATION = "initial location"
    FINAL_LOCATION = "final location"
    DISTANCE = "distance"
    AMOUNT = "amount"


class Tense(Enum):
    PAST = "past"
    PRESENT = "present"
    FUTURE = "future"
    ANY = "any"

    def to_dict(self):
        return self.value


class DSAction(Enum):
    INIT = "INIT"
    INIT_EYE_DIALOGUE = "INIT_EYE_DIALOGUE"
    USER_SENT_UTTERANCE_EYE_DIALOGUE = "USER_SENT_UTTERANCE_EYE_DIALOGUE"
    USER_CHOSE_ACTIONS = "USER_CHOSE_ACTIONS"
    START_DIALOGUE = "START_DIALOGUE"
    DIALOGUE_STARTED = "DIALOGUE_STARTED"
    DISPLAY_UTTERANCE = "DISPLAY_UTTERANCE"
    LOG_ACTION_START = "LOG_ACTION_START"
    LOG_ACTION_COMPLETED = "LOG_ACTION_COMPLETED"
    LOG_ACTION_FAILED = "LOG_ACTION_FAILED"
    LOG_ACTION_SKIPPED = "LOG_ACTION_SKIPPED"
    DISPLAY_LOG = "DISPLAY_LOG"
    REQUEST_USER_CHOOSE_UTTERANCE = "REQUEST_USER_CHOOSE_UTTERANCE"
    REQUEST_USER_CHOOSE_MENU_OPTION = "REQUEST_USER_CHOOSE_MENU_OPTION"
    USER_CHOSE_UTTERANCE = "USER_CHOSE_UTTERANCE"
    USER_CHOSE_MENU_OPTION = "USER_CHOSE_MENU_OPTION"
    USER_SENT_UTTERANCE = "USER_SENT_UTTERANCE"
    SYSTEM_SENT_UTTERANCE = "SYSTEM_SENT_UTTERANCE"
    SESSIONS_INFO = "SESSIONS_INFO"
    ACTIONS_INFO = "ACTIONS_INFO"
    EFFECTS_INFO = "EFFECTS_INFO"
    REQUEST_UTTERANCE_BY_ACTION = "REQUEST_UTTERANCE_BY_ACTION"
    SEND_UTTERANCE_BY_ACTION = "SEND_UTTERANCE_BY_ACTION"
    REQUEST_UTTERANCE_BY_STRING_MATCH = "REQUEST_UTTERANCE_BY_STRING_MATCH"
    REQUEST_UTTERANCE_BY_LLM = "REQUEST_UTTERANCE_BY_LLM"
    SEND_UTTERANCE_BY_STRING_MATCH = "SEND_UTTERANCE_BY_STRING_MATCH"
    REQUEST_USER_CHOOSE_AGENT = "REQUEST_USER_CHOOSE_AGENT"
    USER_CHOSE_AGENT = "USER_CHOSE_AGENT"
    REQUEST_USER_CHOOSE_SCENARIO = "REQUEST_USER_CHOOSE_SCENARIO"
    USER_CHOSE_SCENARIO = "USER_CHOSE_SCENARIO"


class DSActionByType(Enum):
    AGENT = "AGENT"
    DIALOGUE_SYSTEM = "DIALOGUE_SYSTEM"
    DIALOGUE_MANAGER = "DIALOGUE_MANAGER"
    WORLD = "WORLD"


class PlaceholderSymbol(Enum):
    X = "x"
    Y = "y"
    Z = "z"
    ALL = "ALL"
    ANY = "ANY"


class Priority(Enum):
    LOW = 0
    MID = 1
    HIGH = 2
