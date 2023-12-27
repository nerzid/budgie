from enum import Enum


class DSTPronoun(Enum):
    I = 'I'
    YOU = 'YOU'
    ANY = 'ANY'
    EVERYONE = 'EVERYONE'

    def __str__(self):
        return "%s" % self.value

    def __repr__(self):
        return "%s" % self.value


pronouns = {
    DSTPronoun.I: None,
    DSTPronoun.YOU: None,
    DSTPronoun.ANY: None,
    DSTPronoun.EVERYONE: None
}
