from enum import Enum


class DSTPronoun(Enum):
    I = 'I'
    YOU = 'YOU'

    def __str__(self):
        return f'{self.name}'


pronouns = {
    DSTPronoun.I: None,
    DSTPronoun.YOU: None
}
