import datetime
import decimal

class Transaction:
    def __init__(self, date, value):
        self.date = datetime.datetime.strptime(date, "%d.%m.%Y").date()
        self.value = decimal.Decimal(value)

    def __repr__(self):
        return self.date.strftime("%d.%m.%Y")+" : " + str(self.value)