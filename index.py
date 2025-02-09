#!/usr/bin/python3

import argparse
from lib.TableGenerator import TableGenerator
from lib.BarGenerator import BarGenerator
from lib.Config import Config
from models.Portfolio import Portfolio

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Investment portfolio tracker.")
parser.add_argument('-p', '--portfolios', type=str, nargs='+', default=["portfolio"], help="Names of the portfolio folders (default is 'portfolio')")
parser.add_argument('-s', '--summary', action='store_true', help="Include summary information")
parser.add_argument('-c', '--currency', type=str, default="EUR", help="Currency for the portfolio (default is 'EUR')")
args = parser.parse_args()

# Iterate over each portfolio and print the results
for portfolio_name in args.portfolios:
    # Load the config for the current portfolio
    config = Config(argparse.Namespace(portfolio=portfolio_name, summary=args.summary, currency=args.currency))

    portfolio = Portfolio(config)

    tableGenerator = TableGenerator(config, portfolio)
    barGenerator = BarGenerator(config, portfolio)
    tableGenerator.toRichTable()
    barGenerator.run()
