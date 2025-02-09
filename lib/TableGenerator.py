from lib.Generator import Generator
import decimal
from rich.table import Table
from rich.style import Style
from rich.text import Text
from lib.Config import Config
from models.Portfolio import Portfolio


class TableGenerator(Generator):
    """Generates the portfolio table."""
    def __init__(self, config: Config, portfolio: Portfolio):
        super().__init__(config, portfolio)
        self.headings = ['Period'] + self.config.getPrettyPlatforms() + ['Total']
        self.table = Table(expand=True)
        self.table.add_column("Period", justify="left")

        for platform in self.portfolio.platforms:
            self.table.add_column(
                Text(f"▉ {platform}", Style(color=self._getColor(platform))),
                justify="right"
            )

        self.table.add_column("Total", justify="right")

    def run(self):
        """Generates and prints the table."""
        if not self.config.summary:
            self.__createDetailRows()
            self.table.add_section()

        # Add summary rows
        self.table.add_row(*self.__createTotalsRow())
        self.table.add_row(*self.__createInvestedRow())
        self.table.add_row(*self.__createValueRow())
        self.table.add_section()
        self.table.add_row(*self.__createPortfolioShareRow())
        self.table.add_row(*self.__createXirrRow())
        self.table.add_row(*self.__createUnrealisedGainLossRow())

        self.console.print(self.table)

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



# # Example Usage
# def main():
#     config = Config()  # Assuming Config is properly initialized
#     portfolio = Portfolio()  # Assuming Portfolio is properly initialized

#     table_generator = TableGenerator(config, portfolio)
#     bar_generator = BarGenerator(config, portfolio)

#     table_generator.run()  # Print the table
#     bar_generator.run()  # Print the bar chart


# if __name__ == "__main__":
#     main()