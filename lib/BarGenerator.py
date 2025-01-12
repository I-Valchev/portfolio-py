from lib.Generator import Generator
from lib.Config import Config
from models.Portfolio import Portfolio
from rich.style import Style
from rich.panel import Panel


class BarGenerator(Generator):
    """Generates the portfolio share bar chart."""
    def __init__(self, config: Config, portfolio: Portfolio):
        super().__init__(config, portfolio)

    def run(self):
        """Generates and prints the portfolio share bar."""
        self.console.print(self.__createShareBar())

    def __createShareBar(self):
        """Creates a bar chart showing the share of each platform."""
        total_value = sum(p.calculateBalance() + p.calculateReturn() for p in self.portfolio.platforms)
        shares = [self.calculatePercentageOfTotal(p.calculateBalance() + p.calculateReturn(), total_value) for p in self.portfolio.platforms]

        bar_length = self.console.width - 4  # Account for padding
        bar = ""

        for platform, share in zip(self.portfolio.platforms, shares):
            color = self._getColor(platform)
            style = Style(bgcolor=color)
            bar += f"[{style}]{' ' * int(bar_length * (share / 100))}[/]"

        return Panel(bar, title="Portfolio Share", width=self.console.width, expand=True)