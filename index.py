#!/usr/bin/python3

import datetime

from lib.Config import Config
from lib.TableGenerator import TableGenerator
from lib.helpers import generateAllPeriods, generatePlatforms

config = Config()

platforms = generatePlatforms(config)
periods = generateAllPeriods(datetime.date(2020, 1, 1), datetime.date.today())

generator = TableGenerator(config)
generator.setRows(periods, platforms)

generator.print()
