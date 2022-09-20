from models.Group import Group
from models.Transaction import Transaction
from models.Valuation import Valuation
from parsers.TransactionParser import TransactionParser
from parsers.ValuationParser import ValuationParser
from dateutil.relativedelta import relativedelta


class Platform(Group):
    def __init__(self, name):
        super().__init__()
        self.name = name

        valuationsFilename = """./data/%s-valuations.txt""" % self.name
        self.valuations = ValuationParser(valuationsFilename).parse()

        transactionsFilename = """./data/%s-transactions.txt""" % self.name
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
