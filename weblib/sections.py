
import streamlit as st

from lib.helpers import availablePortfolios


def inputs():

    col1, col2 = st.columns(2)

    portfolio = col1.selectbox('Portfolio', availablePortfolios())
    currency = col2.selectbox('Currency', ['EUR', 'BGN'])

    return [portfolio, currency]
