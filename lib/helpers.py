from dateutil.relativedelta import relativedelta

from lib import Config
from lib.Entities.GroupEntities import PeriodEntity, PlatformEntity
from lib.db.Database import Database


def generateAllPeriods(start, end):
    periods = []

    while (start < end):
        next = start + relativedelta(months=+1)
        currentEnd = next + relativedelta(days=-1)

        periods.append(PeriodEntity(start, currentEnd))
        start = next

    return periods

def generatePlatforms(config: Config):
    names = config.getPlatforms()
    return list(map(lambda name: PlatformEntity(name, config), names))


def availablePortfolios():
    return Database().fetchAllPortfolioNames()
