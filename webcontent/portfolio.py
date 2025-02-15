
import datetime
from turtle import st
from lib.db.Database import Database
from lib.db.Models import DbTransaction, DbValuation
from lib.helpers import generateAllPeriods
from webcontent import sections


database = Database()
portfolioName = "Missing"

st.write(f"## {portfolioName}")
portfolio = database.fetchPortfolioByName(portfolioName)
sections.key_metrics(portfolio, portfolio.currency, st)
sections.portfolio_bar(portfolio)

tabs = st.tabs([str(platform) for platform in portfolio.platforms] + ["*+*"])

periods = generateAllPeriods(datetime.datetime(2025, 1, 1), datetime.datetime.today())

for platform, tab in zip(portfolio.platforms, tabs[:-1]):
    sections.key_metrics(platform, portfolio.currency, tab)
    sections.platform_metrics(platform, portfolio, tab)
    tab.divider()
    sections.platform_returns(platform, periods, tab)
    with tab.expander("Valuations"):
        sections.display_and_edit_objects(portfolio, platform, platform.valuations, DbValuation, st)
    with tab.expander("Transactions"):
        sections.display_and_edit_objects(portfolio, platform, platform.transactions, DbTransaction, st)

with tabs[-1]:
    sections.add_new_platform(portfolio, st)