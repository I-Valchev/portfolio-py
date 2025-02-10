from models.Group import Group
from models.Transaction import Transaction
from models.Valuation import Valuation
from dateutil.relativedelta import relativedelta


class Platform(Group):
    def __init__(self):
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

    # TODO: maybe this shouldn't be here
    def __str__(self):
        return self.pretty