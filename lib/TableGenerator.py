import decimal
from rich.console import Console
from rich.table import Table
from lib.Config import Config
from models import Period, Platform
from models.Portfolio import Portfolio


class TableGenerator:
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.headings = ['Period'] + self.config.getPrettyPlatforms() + ['Total']
        
        self.table = Table()
        self.table.add_column("Period", justify="left")
        [self.table.add_column(platform, justify="right") for platform in self.config.getPrettyPlatforms()]
        self.table.add_column("Total", justify="right")

    def print(self):
        self.console.print(self.table)

    def setRows(self, periods: [Period], portfolio: Portfolio):
        platforms = portfolio.platforms  # Get the list of platforms from the Portfolio object

        if not self.config.summary:
            self.__createDetailRows(periods, platforms)

        # Add the summary rows
        self.table.add_row('')
        self.table.add_row(*self.__createTotalsRow(platforms))
        self.table.add_row(*self.__createInvestedRow(platforms))
        self.table.add_row(*self.__createValueRow(platforms))
        self.table.add_row('')
        self.table.add_row(*self.__createPortfolioShareRow(platforms, portfolio))
        self.table.add_row(*self.__createXirrRow(platforms))
        self.table.add_row(*self.__createUnrealisedGainLossRow(portfolio))  # Pass portfolio instead of platforms

    def __createDetailRows(self, periods, platforms):
        rows = self.__initRows(periods, platforms)
        for i, row in enumerate(rows[::-1]):
            if i > 12:
                break

            self.table.add_row(*row)

    def __createRow(self, label: str, platforms: [Platform], calc_func, add_total=False):
        """Helper method to create a row for various calculations."""
        row = [label]
        values = [str(calc_func(p)) for p in platforms]
        row.extend(values)
        if add_total:
            total = self.__getRowSum(values)  # Calculate sum of values
            row.append(total)
        else:
            row.append('')  # Empty total for XIRR
        return row

    def __createValueRow(self, platforms: [Platform]):
        """Creates the Value row for the table."""
        return self.__createRow('Value', platforms, lambda p: p.calculateBalance() + p.calculateReturn(), add_total=True)

    def __createInvestedRow(self, platforms: [Platform]):
        """Creates the Invested row for the table."""
        return self.__createRow('Invested', platforms, lambda p: p.calculateBalance(), add_total=True)

    def __createXirrRow(self, platforms: [Platform]):
        """Creates the xirr row for the table."""
        return self.__createRow('xirr (%)', platforms, lambda p: p.calculateXirr(), add_total=False)

    def __createUnrealisedGainLossRow(self, portfolio: Portfolio):
        """Creates the Unrealised Gain/Loss row for the table."""
        row = ['Unrealised Gain/Loss (%)']
        row.extend(str(p.unrealisedGainLoss()) for p in portfolio.platforms)
        row.append(str(portfolio.calculateTotalUnrealizedGainLoss()))
        return row

    def __createTotalsRow(self, platforms: [Platform]):
        """Creates the Earned row for the table."""
        return self.__createRow('Earned', platforms, lambda p: p.calculateReturn(), add_total=True)

    def __createPortfolioShareRow(self, platforms: [Platform], portfolio: Portfolio):
        """Creates the Portfolio Share row for the table."""
        total_value = portfolio.calculatePortfolioValue()
        return self.__createRow('% of portfolio', platforms, lambda p: p.calculatePortfolioShare(total_value), add_total=False)

    def __initRows(self, periods: [Period], platforms: [Platform]):
        rows = []
        for period in periods:
            row = []
            for platform in platforms:
                period.fill(platform.valuations, platform.transactions)
                row.append(str(period.calculateReturn()))

            row.append(self.__getRowSum(row))
            row.insert(0, period.start.strftime('%B %Y'))

            rows.append(row)

        return rows

    def __getRowSum(self, values: [str]):
        """Calculate the sum of a list of string values."""
        return str(sum(map(lambda v: decimal.Decimal(v), values)))
