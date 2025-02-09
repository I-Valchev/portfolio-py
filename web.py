import streamlit as st
import argparse
from lib.Config import Config
from lib.TableGenerator import TableGenerator
from models.Portfolio import Portfolio
import pandas as pd
import plotly.express as px
from weblib import sections

st.write('# Portfolio Tracker')

# INPUTS
[portfolio, currency] = sections.inputs()

config = Config(argparse.Namespace(portfolio=portfolio, currency=currency))
portfolio = Portfolio(config)

# METRICS
col1, col2 = st.columns(2)
with col1:
    delta = portfolio.calculatePortfolioValue() - portfolio.calculatePortfolioBalance()
    st.metric(label='Portfolio Value', value=f"{portfolio.calculatePortfolioValue()} {config.currency}", delta=f"{delta}")

with col2:
    st.metric(label='Unrealized Gain/Loss', value=f"{portfolio.calculateTotalUnrealizedGainLoss()} %")

# Extract names and balances
platform_names = [str(platform) for platform in portfolio.platforms]
platform_balances = [int(platform.calculateCurrentValue()) for platform in portfolio.platforms]
platform_colors = [config.config['platforms'][platform.name]['color'] for platform in portfolio.platforms]

# Create a pandas DataFrame
data = pd.DataFrame({
    "Platform": platform_names,
    "Value": platform_balances,
})

st.bar_chart(data, x='Platform', y='Value')


tableGenerator = TableGenerator(config, portfolio)
table = tableGenerator.toArray()

st.table(table)
