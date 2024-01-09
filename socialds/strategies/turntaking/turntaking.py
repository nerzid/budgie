from enum import Enum


class TurnTaking(Enum):
    AfterUserChoseUtterance = 'After User Chose Utterance'
    AfterUserExecutedAllActions = 'After User Executed All Actions'
    WheneverPossible = 'Whenever Possible'
