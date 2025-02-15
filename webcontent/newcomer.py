import streamlit as st
from lib.Entities.Portfolio import PortfolioEntity
from lib.db.Database import Database


def newcomper(st: st):
    st.write('# Start your investment journey!') 
    st.write('It looks like you don\'t have any portfolios yet. Track your investment journey by adding a new portfolio!')

def add_new_portfolio(target: st):
    target.write('## Add a new Portfolio')

    portfolio_name = target.text_input('Portfolio Name')
    portfolio_currency = target.selectbox('Currency', ['EUR'])
    
    if target.button("Create Portfolio"):
        if portfolio_name:
            # Create the new portfolio using the new factory method
            new_portfolio = PortfolioEntity.new(name=portfolio_name, currency=portfolio_currency)
            result = Database().add_new_portfolio(new_portfolio)
            st.rerun()
            if result:
                target.success(result.message)
            else:
                target.warning(result.message)
        else:
            target.warning("Please enter a portfolio name")
