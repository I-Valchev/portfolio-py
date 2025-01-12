import datetime
import decimal
from lib import Config
from lib.helpers import generateAllPeriods
from models.Portfolio import Portfolio
from rich.console import Console


class Generator:
    """Base class containing common properties and methods for generators."""
    def __init__(self, config: Config, portfolio: Portfolio):
        self.config = config
        self.console = Console()
        self.portfolio = portfolio
        self.periods = generateAllPeriods(datetime.date(2020, 1, 1), datetime.date.today())

    def calculatePercentageOfTotal(self, value, total):
        """Calculates the value as a percentage of the total."""
        if total == 0:
            return decimal.Decimal("0.00")  # Avoid division by zero
        return (decimal.Decimal(value) / decimal.Decimal(total) * 100).quantize(decimal.Decimal("0.00"))

    def _getColor(self, platform):
        """Returns the color for a given platform."""
        return self.config.config['platforms'][platform.name]['color']