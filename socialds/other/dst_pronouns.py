from enum import Enum


class DSTPronoun(Enum):
    I = "I"
    YOU = "YOU"
    ANY = "ANY"
    EVERYONE = "EVERYONE"

    def __str__(self):
        return "%s" % self.value

    def __repr__(self):
        return "%s" % self.value


def get_agent(agent, pronouns):
    if isinstance(agent, DSTPronoun):
        if agent == DSTPronoun.ANY:
            from socialds.any.any_agent import AnyAgent

            return AnyAgent()
        else:
            return pronouns[agent]
    return agent


def pronounify(thing, pronouns):
    if isinstance(thing, DSTPronoun):
        return pronouns[thing]
    return thing
