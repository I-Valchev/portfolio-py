from lib import Config
from models import Valuation


class ValuationParser:
    def __init__(self, file):
        self.file = file

    def parse(self, config: Config):
        lines = tuple(open(self.file, 'r'))
        currencyAdjustment = config.getCurrencyAdjustment()
        return [self.__lineToValution(line, currencyAdjustment) for line in lines]

    def __lineToValution(self, line, currencyAdjustment):
        date, value = line.split(" ")
        return Valuation.Valuation(date, value, currencyAdjustment)
