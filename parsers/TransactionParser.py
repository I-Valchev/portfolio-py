from models import Transaction


class TransactionParser:
    def __init__(self, file):
        self.file = file

    def parse(self):
        lines = tuple(open(self.file, 'r'))
        return list(map(self.__lineToTransaction, lines))

    def __lineToTransaction(self, line):
        date, value = line.split(" ")
        return Transaction.Transaction(date, value)
