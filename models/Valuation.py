import datetime
import decimal

class Valuation:
    def __init__(self, date, value):
        self.date = date if type(date) is datetime.date else datetime.datetime.strptime(date, "%d.%m.%Y").date()
        self.value = decimal.Decimal(eval(str(value))).quantize(decimal.Decimal("0.00")) # Ensure value is a string before evaluating

    def __repr__(self):
        return self.date.strftime("%d.%m.%Y")+" : " + str(self.value)