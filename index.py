#!/usr/bin/python3

import datetime
import argparse

from lib.Config import Config
from lib.TableGenerator import TableGenerator
from lib.helpers import generateAllPeriods
from models.Portfolio import Portfolio

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Investment portfolio tracker.")
parser.add_argument('-p', '--portfolios', type=str, nargs='+', default=["portfolio"], help="Names of the portfolio folders (default is 'portfolio')")
parser.add_argument('-s', '--summary', action='store_true', help="Include summary information")
args = parser.parse_args()

# Iterate over each portfolio and print the results
for portfolio_name in args.portfolios:
    # Load the config for the current portfolio
    config = Config(argparse.Namespace(portfolio=portfolio_name, summary=args.summary))

    portfolio = Portfolio(config)
    periods = generateAllPeriods(datetime.date(2020, 1, 1), datetime.date.today())

    generator = TableGenerator(config)
    generator.setRows(periods, portfolio)

    generator.print()
