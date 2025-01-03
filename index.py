#!/usr/bin/python3

import datetime
import argparse

from lib.Config import Config
from lib.TableGenerator import TableGenerator
from lib.helpers import generateAllPeriods, generatePlatforms

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Investment portfolio tracker.")
parser.add_argument('-p', '--portfolio', type=str, default="data", help="Name of the portfolio folder (default is 'data')")
args = parser.parse_args()

# Load the config
config = Config(args.portfolio)

platforms = generatePlatforms(config)
periods = generateAllPeriods(datetime.date(2020, 1, 1), datetime.date.today())

generator = TableGenerator(config)
generator.setRows(periods, platforms)

generator.print()
