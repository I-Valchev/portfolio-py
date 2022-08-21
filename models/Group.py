import pyxirr

from models.Transaction import Transaction


class Group:
    def __init__(self):
        self.valuations = None
        self.transactions = None

    def calculateBalance(self):
        return sum(map(lambda t: t.value, self.transactions))

    def calculateXirr(self):
        interestTransaction = Transaction(self.valuations[-1].date, -self.valuations[-1].value)
        flows = self.transactions + [interestTransaction]

        dates = list(map(lambda f: f.date, flows))
        amounts = list(map(lambda f: -f.value, flows))

        return round(pyxirr.xirr(dates, amounts) * 100, 2)

    def calculateReturn(self):
        if not self.valuations:
            return 0

        earliest = self.valuations[0]
        latest = self.valuations[-1]

        value = latest.value - earliest.value
        balance = sum(
            map(lambda t: t.value if t.date >= earliest.date and t.date <= latest.date else 0, self.transactions))

        return value - balance

    def _qualifyTransactions(self, transactions: [Transaction]):
        if not self.valuations:
            return None

        lastValuation = self.valuations[-1]

        return list(filter(lambda t: t.date <= lastValuation.date, transactions))
