import datetime
import decimal
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.panel import Panel
from rich.text import Text
from lib.Config import Config
from lib.helpers import generateAllPeriods
from models.Portfolio import Portfolio

class TableGenerator:
    def __init__(self, config: Config, portfolio: Portfolio):
        self.config = config
        self.console = Console()
        self.portfolio = portfolio
        self.periods = generateAllPeriods(datetime.date(2020, 1, 1), datetime.date.today())
        self.headings = ['Period'] + self.config.getPrettyPlatforms() + ['Total']
        
        self.table = Table(expand=True)
        self.table.add_column("Period", justify="left")

        [self.table.add_column(
            Text(f"▉ {platform}", Style(color=self.__getColor(platform))), 
            justify="right"
        ) for platform in self.portfolio.platforms]
        self.table.add_column("Total", justify="right")

    def run(self):
        self.portfolio.platforms  # Get the list of platforms from the Portfolio object

        if not self.config.summary:
            self.__createDetailRows()
            self.table.add_section()

        # Add the summary rows
        self.table.add_row(*self.__createTotalsRow())
        self.table.add_row(*self.__createInvestedRow())
        self.table.add_row(*self.__createValueRow())
        self.table.add_section()
        self.table.add_row(*self.__createPortfolioShareRow())
        self.table.add_row(*self.__createXirrRow())
        self.table.add_row(*self.__createUnrealisedGainLossRow())

        self.console.print(self.table)
        self.console.print(self.__createShareBar())  # Print the share bar underneath the table

    def __createDetailRows(self):
        rows = self.__initRows()
        for i, row in enumerate(rows[::-1]):
            if i > 12:
                break

            self.table.add_row(*row)

    def __createRow(self, label: str, calc_func, add_total=False):
        """Helper method to create a row for various calculations."""
        row = [label]
        values = [str(calc_func(p)) for p in self.portfolio.platforms]
        row.extend(values)
        if add_total:
            total = self.__getRowSum(values)  # Calculate sum of values
            row.append(total)
        else:
            row.append('')  # Empty total for XIRR
        return row

    def __createValueRow(self):
        """Creates the Value row for the table."""
        return self.__createRow('Value', lambda p: p.calculateBalance() + p.calculateReturn(), add_total=True)

    def __createInvestedRow(self):
        """Creates the Invested row for the table."""
        return self.__createRow('Invested', lambda p: p.calculateBalance(), add_total=True)

    def __createXirrRow(self):
        """Creates the xirr row for the table."""
        return self.__createRow('xirr (%)', lambda p: p.calculateXirr(), add_total=False)

    def __createUnrealisedGainLossRow(self):
        """Creates the Unrealised Gain/Loss row for the table."""
        row = ['Unrealised Gain/Loss (%)']
        row.extend(str(p.unrealisedGainLoss()) for p in self.portfolio.platforms)
        row.append(str(self.portfolio.calculateTotalUnrealizedGainLoss()))
        return row

    def __createTotalsRow(self):
        """Creates the Earned row for the table."""
        return self.__createRow('Earned', lambda p: p.calculateReturn(), add_total=True)

    def __createPortfolioShareRow(self):
        """Creates the Portfolio Share row for the table."""
        total_value = sum(p.calculateBalance() + p.calculateReturn() for p in self.portfolio.platforms)
        row = ['Portfolio Share (%)']
        shares = [self.calculatePercentageOfTotal(p.calculateBalance() + p.calculateReturn(), total_value) for p in self.portfolio.platforms]
        row.extend(str(share) for share in shares)
        row.append('100.00')  # Total percentage is always 100%
        return row

    def calculatePercentageOfTotal(self, value, total):
        """Calculates the value as a percentage of the total."""
        if total == 0:
            return decimal.Decimal("0.00")  # Avoid division by zero
        return (decimal.Decimal(value) / decimal.Decimal(total) * 100).quantize(decimal.Decimal("0.00"))

    def __createShareBar(self):
        """Creates a bar chart showing the share of each platform."""
        total_value = sum(p.calculateBalance() + p.calculateReturn() for p in self.portfolio.platforms)
        shares = [self.calculatePercentageOfTotal(p.calculateBalance() + p.calculateReturn(), total_value) for p in self.portfolio.platforms]

        bar_length = self.console.width
        bar = ""
        for platform, share in zip(self.portfolio.platforms, shares):
            color = self.__getColor(platform)
            style = Style(bgcolor=color)
            bar += f"[{style}]{' ' * int(bar_length * (share / 100))}[/]"
        return Panel(bar, title="Portfolio Share")

    def __getColor(self, platform):
        """Returns the color for a given platform."""
        return self.config.config['platforms'][platform.name]['color']

    def __initRows(self):
        rows = []
        for period in self.periods:
            row = []
            for platform in self.portfolio.platforms:
                period.fill(platform.valuations, platform.transactions)
                row.append(str(period.calculateReturn()))

            row.append(self.__getRowSum(row))
            row.insert(0, period.start.strftime('%B %Y'))

            rows.append(row)

        return rows

    def __getRowSum(self, values: [str]):
        """Calculate the sum of a list of string values."""
        return str(sum(map(lambda v: decimal.Decimal(v), values)))
