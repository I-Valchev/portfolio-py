import decimal

from rich.console import Console
from rich.table import Table
from lib.Config import Config
from models import Period, Platform


class TableGenerator:
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()

        self.headings = ['Date'] + self.config.getPrettyPlatforms() + ['Total']
        self.table = Table(*self.headings)

    def print(self):
        self.console.print(self.table)

    def setRows(self, periods: [Period], platforms: [Platform]):
        rows = self.__initRows(periods, platforms)
        for i, row in enumerate(rows[::-1]):
            if i > 12:
                break

            self.table.add_row(*row)

        self.table.add_row('---')
        self.table.add_row(*self.__createTotalsRow(platforms))

    def __createTotalsRow(self, platforms: [Platform]):
        row = ['TOTAL']
        for p in platforms:
            row.append(str(p.calculateReturnBy()))

        row.append(self.__getRowSum(row))

        return row

    def __initRows(self, periods: [Period], platforms: [Platform]):
        rows = []
        for period in periods:
            row = []
            row.append(period.start.strftime('%B %Y'))
            for platform in platforms:
                period.fill(platform.valuations, platform.transactions)

                row.append(str(period.calculateReturnBy()))

            row.append(self.__getRowSum(row))

            rows.append(row)

        return rows

    def __getRowSum(self, row: []):
        return str(sum(map(lambda v: decimal.Decimal(v), row[1:])))