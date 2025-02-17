import datetime
from lib.db.Models import DbTransaction, DbValuation


class TransactionEntity:
    def __init__(self, dbTransaction: DbTransaction):
        self._dbTransaction = dbTransaction
    
    @property
    def date(self):
        date = self._dbTransaction.date
        return date if type(date) is datetime.datetime else datetime.datetime.strptime(date, "%d.%m.%Y").date()
    
    @property
    def value(self):
        return self._dbTransaction.value
    
    def __repr__(self):
        return self.date.strftime("%d.%m.%Y")+" : " + str(self.value)

class ValuationEntity:
    def __init__(self, dbValuation: DbValuation):
        self._dbValuation = dbValuation

    @classmethod
    def new(cls, date: datetime.datetime = datetime.datetime.now(), value: float = 0):
        return cls(DbValuation(date=date, value=value))

    @property
    def date(self):
        date = self._dbValuation.date
        return date if type(date) is datetime.datetime else datetime.datetime.strptime(date, "%d.%m.%Y").date()
    
    @property
    def value(self):
        return self._dbValuation.value
    
    def __repr__(self):
        return self.date.strftime("%d.%m.%Y")+" : " + str(self.value)