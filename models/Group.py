import pyxirr
from datetime import date
from models.Transaction import Transaction


class Group:
    def __init__(self):
        self.valuations = []
        self.transactions = []

    def calculateBalance(self):
        """Sum of all transaction values (net inflow)."""
        return sum(t.value for t in self.transactions)

    def calculateXirr(self):
        """Computes XIRR based on transactions and valuations."""
        if not self.valuations and not self.transactions:
            interestTransaction = Transaction(date.today(), 0)
        elif not self.valuations and self.transactions:
            interestTransaction = Transaction(self.transactions[-1].date, 0)
        else:
            interestTransaction = Transaction(self.valuations[-1].date, -self.valuations[-1].value)

        flows = self.transactions + [interestTransaction]
        dates = [t.date for t in flows]
        amounts = [-t.value for t in flows]  # XIRR expects outflows as negative

        try:
            return round(pyxirr.xirr(dates, amounts, guess=0) * 100, 2)
        except:
            return None

    def _netInvestments(self, start_date, end_date):
        """Returns total net investments (inflows - outflows) between two dates."""
        return sum(t.value for t in self.transactions if start_date <= t.date <= end_date)

    def calculateReturn(self):
        """
        Total return = (Final Valuation - Initial Valuation) - Net Investments.
        """
        if not self.valuations:
            return 0

        initial_valuation = self.valuations[0]
        final_valuation = self.valuations[-1]

        net_investments = self._netInvestments(initial_valuation.date, final_valuation.date)

        return (final_valuation.value - initial_valuation.value) - net_investments

    def unrealisedGainLoss(self):
        """
        Calculates the unrealized gain/loss as a percentage.
        Formula:
            Unrealized Gain/Loss % = (Latest Valuation - Net Investments) / Net Investments * 100
        """
        if not self.valuations:
            return 0

        latest = self.valuations[-1]
        net_investments = self._netInvestments(self.valuations[0].date, latest.date)

        if net_investments == 0:
            return 0  # Avoid division by zero

        unrealized_percentage = ((latest.value - net_investments) / net_investments) * 100
        return round(unrealized_percentage, 2)

    def _qualifyTransactions(self, transactions: [Transaction]):
        """Filters transactions that occurred before the latest valuation."""
        if not self.valuations:
            return transactions

        lastValuation = self.valuations[-1]
        return [t for t in transactions if t.date <= lastValuation.date]
