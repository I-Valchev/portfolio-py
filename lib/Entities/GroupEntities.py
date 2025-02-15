import decimal
import re
from lib.Entities.BasicEntities import TransactionEntity, ValuationEntity
from lib.db.Models import DbPlatform
from dateutil.relativedelta import relativedelta


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
            interestTransaction = TransactionEntity(date.today(), 0)
        elif not self.valuations and self.transactions:
            interestTransaction = TransactionEntity(self.transactions[-1].date, 0)
        else:
            interestTransaction = TransactionEntity(self.valuations[-1].date, -self.valuations[-1].value)

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

    def _qualifyTransactions(self, transactions: [TransactionEntity]):
        """Filters transactions that occurred before the latest valuation."""
        if not self.valuations:
            return transactions

        lastValuation = self.valuations[-1]
        return [t for t in transactions if t.date <= lastValuation.date]


class PlatformEntity(Group):
    def __init__(self, dbPlatform: DbPlatform):
        self._dbPlatform = dbPlatform
        self.__fillInitialValuation(self.transactions)

    @classmethod
    def new(cls, name: str = None, pretty: str = None, color: str = None):
        """Factory method to create a new PlatformEntity at runtime"""
        if pretty and not name:
            name = re.sub(r"\s+", "_", pretty.lower())  # Convert spaces to underscores and lowercase it
        
        if not name:
            raise ValueError("A platform must have a name or a pretty name.")

        dbPlatform = DbPlatform(
            name=name,
            pretty=pretty or name,
            color=color or "#000000",
            transactions=[],
            valuations=[]
        )
        return cls(dbPlatform)

    @property
    def name(self):
        return self._dbPlatform.name
    
    @property
    def pretty(self):
        return self._dbPlatform.pretty
    
    @property
    def color(self):
        return self._dbPlatform.color   
    
    @property
    def transactions(self):
        return list(map(lambda t: TransactionEntity(t), self._dbPlatform.transactions))
    
    @property
    def valuations(self):
        return list(map(lambda v: ValuationEntity(v), self._dbPlatform.valuations))
    
    def __repr__(self):
        return self.pretty

    def __str__(self):
        return self.pretty
    
    def __fillInitialValuation(self, transactions: list[TransactionEntity]):
        if not self.valuations:
            return

        valuation = self.valuations[0]
        transactionsBeforeValuation = list(filter(lambda t: t.date <= valuation.date, transactions))

        if not transactionsBeforeValuation:
            return

        earliest = transactionsBeforeValuation[0]

        initial = ValuationEntity.new(earliest.date + relativedelta(days=-1), 0)
        self.valuations.insert(0, initial)


class PeriodEntity(Group):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end

    def fill(self, valuations: list[ValuationEntity], transactions: list[TransactionEntity]):
        self.__fillValuations(valuations)
        self.__fillTransactions(transactions)
    
    def __fillValuations(self, valuations: list[ValuationEntity]):
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

    def __fillTransactions(self, transactions: list[TransactionEntity]):
        self.transactions = self._qualifyTransactions(transactions)


    def __tooEarly(self, date):
        return self.start > date

    def __tooLate(self, date):
        return self.end < date

    def __repr__(self):
        return self.start.strftime("%d.%m.%Y")+" : " + self.end.strftime("%d.%m.%Y")