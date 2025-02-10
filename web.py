import datetime
import numpy as np
import streamlit as st
import argparse
from lib.Config import Config
from lib.TableGenerator import TableGenerator
from lib.helpers import generateAllPeriods
from models.Portfolio import Portfolio
import pandas as pd
from webcontent import newcomer, sections
from streamlit_gsheets import GSheetsConnection
from lib.db.Database import Database

st.write('# Portfolio Tracker')

database = Database()

# INPUTS
[portfolioName, currency] = sections.inputs()
st.divider()

if portfolioName == None:
    newcomer.newcomper(st)
else:
    portfolio = database.fetchPortfolioByName(portfolioName)
    sections.key_metrics(portfolio, portfolio.currency, st)
    sections.portfolio_bar(portfolio)

    tabs = st.tabs([str(platform) for platform in portfolio.platforms])

    periods = generateAllPeriods(datetime.datetime(2024, 1, 1), datetime.datetime.today())

    for platform, tab in zip(portfolio.platforms, tabs):
        sections.key_metrics(platform, portfolio.currency, tab)
        sections.platform_metrics(platform, portfolio, tab)
        sections.platform_returns(platform, periods, tab)
