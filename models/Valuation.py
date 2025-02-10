import datetime
import decimal

class Valuation:
    def __init__(self, date, value, currencyAdjustment=1.0):
        self.date = date if type(date) is datetime.datetime else datetime.datetime.strptime(date, "%d.%m.%Y").date()
        self.value = float(eval(str(value))*(currencyAdjustment))


    def __repr__(self):
        return self.date.strftime("%d.%m.%Y")+" : " + str(self.value)