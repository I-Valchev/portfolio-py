from models import Valuation


class ValuationParser:
    def __init__(self, file):
        self.file = file

    def parse(self):
        lines = tuple(open(self.file, 'r'))
        return list(map(self.__lineToValution, lines))

    def __lineToValution(self, line):
        date, value = line.split(" ")
        return Valuation.Valuation(date, value)
