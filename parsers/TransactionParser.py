from lib import Config
from models import Transaction


class TransactionParser:
    def __init__(self, file):
        self.file = file

    def parse(self, config: Config):
        lines = tuple(open(self.file, 'r'))
        currencyAdjustment = config.getCurrencyAdjustment()
        return [self.__lineToTransaction(line, currencyAdjustment) for line in lines]

    def __lineToTransaction(self, line, currencyAdjustment):
        date, value = line.split(" ")
        return Transaction.Transaction(date, value, currencyAdjustment)
