from enum import Enum

class TermColor(Enum):
    LIGHT_BLUE = 'light_blue'
    LIGHT_YELLOW = 'light_yellow'
    LIGHT_RED = 'light_red'
    LIGHT_GREEN = 'light_green'
    LIGHT_CYAN = 'light_cyan'
    LIGHT_MAGENTA = 'light_magenta'
    RED = 'red'
    BLACK = 'black'
    GREY = 'grey'
    GREEN = 'green'
    ON_RED = 'on_red'
    ON_CYAN = 'on_cyan'
    ON_BLUE = 'on_blue'
    ON_WHITE = 'on_white'
    ON_GREEN = 'on_green'
    ON_MAGENTA = 'on_magenta'
    ON_YELLOW = 'on_yellow'
    ON_LIGHT_MAGENTA = 'on_light_magenta'


class SemanticEvent(Enum):
    AGENT = 'agent'
    PARTNER = 'partner'
    CAUSE = 'cause'
    INSTRUMENT = 'instrument'
    PATIENT = 'patient'
    THEME = 'theme'
    BENEFICIARY = 'beneficiary'
    GOAL = 'goal'
    SOURCE = 'source'
    RESULT = 'result'
    REASON = 'reason'
    PURPOSE = 'purpose'
    MANNER = 'manner'
    MEDIUM = 'medium'
    MEANS = 'means'
    TIME = 'time'
    INITIAL_TIME = 'initial time'
    FINAL_TIME = 'final time'
    DURATION = 'duration'
    SETTING = 'setting'
    LOCATION = 'location'
    INITIAL_LOCATION = 'initial location'
    FINAL_LOCATION = 'final location'
    DISTANCE = 'distance'
    PATH = 'path'
    FREQUENCY = 'frequency'
    AMOUNT = 'amount'


class SemanticState(Enum):
    ATTRIBUTE = 'attribute'
    PIVOT = 'PIVOT'
    INSTRUMENT = 'instrument'
    SETTING = 'setting'
    THEME = 'theme'
    BENEFICIARY = 'beneficiary'
    REASON = 'reason'
    TIME = 'time'
    INITIAL_TIME = 'initial time'
    FINAL_TIME = 'final time'
    DURATION = 'duration'
    MANNER = 'manner'
    LOCATION = 'location'
    INITIAL_LOCATION = 'initial location'
    FINAL_LOCATION = 'final location'
    DISTANCE = 'distance'
    AMOUNT = 'amount'


class Tense(Enum):
    PAST = 'past'
    PRESENT = 'present'
    FUTURE = 'future'
    ANY = 'any'


class DSAction(Enum):
    DISPLAY_UTTERANCE = 'DISPLAY_UTTERANCE'
    LOG_ACTION_START = 'LOG_ACTION_START'
    LOG_ACTION_COMPLETED = 'LOG_ACTION_COMPLETED'
    LOG_ACTION_SKIPPED = 'LOG_ACTION_SKIPPED'
    DISPLAY_LOG = 'DISPLAY_LOG'
    REQUEST_USER_CHOOSE_UTTERANCE = 'REQUEST_USER_CHOOSE_UTTERANCE'
    REQUEST_USER_CHOOSE_MENU_OPTION = 'REQUEST_USER_CHOOSE_MENU_OPTION'
    USER_CHOSE_UTTERANCE = 'USER_CHOSE_UTTERANCE'
    USER_CHOSE_MENU_OPTION = 'USER_CHOSE_MENU_OPTION'
    START_DIALOGUE = 'START_DIALOGUE'


class DSActionByType(Enum):
    AGENT = 'AGENT'
    DIALOGUE_SYSTEM = 'DIALOGUE_SYSTEM'
    WORLD = 'WORLD'
