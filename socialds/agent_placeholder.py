from socialds.enums import PlaceholderSymbol


class AgentPlaceholder:
    def __init__(self, symbol: PlaceholderSymbol, agent=None) -> None:
        self.symbol = symbol  # the place holder symbol is used to distinguish agents without storing them at first
        self.agent = agent
