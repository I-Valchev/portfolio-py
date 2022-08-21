from models import Valuation
from models.Group import Group
from models.Transaction import Transaction


class Period(Group):
    def __init__(self, start, end):
        super().__init__()

        self.valuations = None
        self.start = start
        self.end = end

    def fill(self, valuations: [Valuation], transactions: [Transaction]):
        self.__fillValuations(valuations)
        self.__fillTransactions(transactions)

    def __fillValuations(self, valuations: [Valuation]):
        self.valuations = []
        prev = None

        for v in valuations:

            if self.__tooEarly(v.date):
                prev = v
                continue

            if self.__tooLate(v.date):
                break

            # if the first one, add the prev too
            if len(self.valuations) == 0 and prev is not None:
                self.valuations.append(prev)

            self.valuations.append(v)

    def __fillTransactions(self, transactions: [Transaction]):
        self.transactions = self._qualifyTransactions(transactions)


    def __tooEarly(self, date):
        return self.start > date

    def __tooLate(self, date):
        return self.end < date

    def __repr__(self):
        return self.start.strftime("%d.%m.%Y")+" : " + self.end.strftime("%d.%m.%Y")
