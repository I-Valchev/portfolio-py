import pandas as pd
from lib.Generator import Generator
import decimal
from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.text import Text
from lib.Config import Config
from models.Portfolio import Portfolio


class TableGenerator(Generator):
    """Generates the portfolio table."""
    def __init__(self, config: Config, portfolio: Portfolio):
        super().__init__(config, portfolio)
        self.config = config
        self.portfolio = portfolio
        self.data = []

        self.__run()

    def __run(self):
        """Generates the table data."""
        if not self.config.summary:
            self.__createDetailRows()
            self.data.append([])  # Add section

        # Add summary rows
        self.data.append(self.__createTotalsRow())
        self.data.append(self.__createInvestedRow())
        self.data.append(self.__createValueRow())
        self.data.append([])
        self.data.append(self.__createPortfolioShareRow())
        self.data.append(self.__createXirrRow())
        self.data.append(self.__createUnrealisedGainLossRow())

        return self.data

    def toArray(self):
        """Returns the table data as a pandas DataFrame."""
        headings = ["Period"] + [str(platform) for platform in self.portfolio.platforms] + ["Total"]
        array_data = [headings]
        for row in self.data:
            if row:
                array_data.append(row)
            else:
                array_data.append([""] * len(headings))  # Add empty row for section
        return pd.DataFrame(array_data[1:], columns=array_data[0])

    def toRichTable(self):
        """Generates and returns the rich table."""
        table = Table(expand=True)
        table.add_column("Period", justify="left")

        for platform in self.portfolio.platforms:
            table.add_column(
                Text(f"▉ {platform}", Style(color=self._getColor(platform))),
                justify="right"
            )

        table.add_column("Total", justify="right")

        for row in self.data:
            if row:
                table.add_row(*row)
            else:
                table.add_section()

        self.console.print(table)

    def __createDetailRows(self):
        rows = self.__initRows()
        for i, row in enumerate(rows[::-1]):
            if i > 12:
                break
            self.data.append(row)

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
        return self.__createRow('Value', lambda p: p.calculateBalance() + p.calculateReturn(), add_total=True)

    def __createInvestedRow(self):
        return self.__createRow('Invested', lambda p: p.calculateBalance(), add_total=True)

    def __createXirrRow(self):
        return self.__createRow('xirr (%)', lambda p: p.calculateXirr(), add_total=False)

    def __createUnrealisedGainLossRow(self):
        row = ['Unrealised Gain/Loss (%)']
        row.extend(str(p.unrealisedGainLoss()) for p in self.portfolio.platforms)
        row.append(str(self.portfolio.calculateTotalUnrealizedGainLoss()))
        return row

    def __createTotalsRow(self):
        return self.__createRow('Earned', lambda p: p.calculateReturn(), add_total=True)

    def __createPortfolioShareRow(self):
        total_value = sum(p.calculateBalance() + p.calculateReturn() for p in self.portfolio.platforms)
        row = ['Portfolio Share (%)']
        shares = [self.calculatePercentageOfTotal(p.calculateCurrentValue(), total_value) for p in self.portfolio.platforms]
        row.extend(str(share) for share in shares)
        return row

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
        return str(sum(map(lambda v: decimal.Decimal(v), values)))