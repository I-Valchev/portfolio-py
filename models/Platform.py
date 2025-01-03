from models.Group import Group
from models.Transaction import Transaction
from models.Valuation import Valuation
from parsers.TransactionParser import TransactionParser
from parsers.ValuationParser import ValuationParser
from dateutil.relativedelta import relativedelta
import os

class Platform(Group):
    def __init__(self, name, config):
        super().__init__()
        self.name = name

        # Use config to get the portfolio directory
        portfolio_dir = config.getPortfolioDir()

        # Construct the paths for valuations and transactions based on portfolio directory
        valuationsFilename = os.path.join(portfolio_dir, f"{self.name}-valuations.txt")
        transactionsFilename = os.path.join(portfolio_dir, f"{self.name}-transactions.txt")
        
        # Parse the valuations and transactions using the new paths
        self.valuations = ValuationParser(valuationsFilename).parse()
        self.transactions = self._qualifyTransactions(TransactionParser(transactionsFilename).parse())

        self.__fillInitialValuation(self.transactions)

    def __fillInitialValuation(self, transactions: [Transaction]):
        if not self.valuations:
            return

        valuation = self.valuations[0]
        transactionsBeforeValuation = list(filter(lambda t: t.date <= valuation.date, transactions))

        if not transactionsBeforeValuation:
            return

        earliest = transactionsBeforeValuation[0]

        initial = Valuation(earliest.date + relativedelta(days=-1), 0)
        self.valuations.insert(0, initial)
