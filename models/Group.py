import pyxirr
import decimal
from datetime import date
from models.Transaction import Transaction
import streamlit as st


class Group:
    def __init__(self):
        self.valuations = []
        self.transactions = []

    def calculateBalance(self) -> float:
        """Sum of all transaction values (net inflow)."""
        # return decimal.Decimal(sum(t.value for t in self.transactions)).quantize(decimal.Decimal("0.00"))
        return sum(t.value for t in self.transactions)
    
    def calculateCurrentValue(self) -> float:
        return self.calculateBalance() + self.calculateReturn()


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
        return sum(t.value for t in self.transactions if start_date < t.date < end_date)

    def calculateReturn(self) -> float:
        """
        Total return = (Final Valuation - Initial Valuation) - Net Investments.
        """
        if not self.valuations:
            return float(0.00)

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
            return float(0.00)

        latest = self.valuations[-1]
        net_investments = self._netInvestments(self.valuations[0].date, latest.date)

        if net_investments == 0:
            return decimal.Decimal("0.00")  # Avoid division by zero

        unrealized_percentage = ((latest.value - net_investments) / net_investments) * 100
        return round(unrealized_percentage, 2)
    
    def calculatePortfolioShare(self, total_value):
        """Calculates the share of the portfolio's value."""
        if total_value == 0:
            return float(0.00)

        return round((self.calculateBalance() + self.calculateReturn()) * 100 / total_value, 2)

    def _qualifyTransactions(self, transactions: [Transaction]):
        """Filters transactions that occurred before the latest valuation."""
        if not self.valuations:
            return transactions

        lastValuation = self.valuations[-1]
        return [t for t in transactions if t.date <= lastValuation.date]
