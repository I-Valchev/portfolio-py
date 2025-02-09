import os
from dateutil.relativedelta import relativedelta

from lib import Config
from models.Period import Period
from models.Platform import Platform


def generateAllPeriods(start, end):
    periods = []

    while (start < end):
        next = start + relativedelta(months=+1)
        currentEnd = next + relativedelta(days=-1)

        periods.append(Period(start, currentEnd))
        start = next

    return periods

def generatePlatforms(config: Config):
    names = config.getPlatforms()
    return list(map(lambda name: Platform(name, config), names))


def availablePortfolios():
    try:
        portfoliosFolder = os.path.join('data-no')
        return [name for name in os.listdir(portfoliosFolder) if os.path.isdir(os.path.join(portfoliosFolder, name))]
    except FileNotFoundError:
        return []