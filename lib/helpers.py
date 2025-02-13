import hashlib
import os
import random
import streamlit as st
from dateutil.relativedelta import relativedelta

from lib import Config
from lib.db.Database import Database
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
    return Database().fetchAllPortfolioNames()
