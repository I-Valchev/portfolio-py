from models.Transaction import Transaction


class Group:
    def __init__(self):
        self.valuations = None
        self.transactions = None

    def calculateReturnBy(self):
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
