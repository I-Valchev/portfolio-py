import datetime
import numpy as np
import streamlit as st
import argparse
from lib.Config import Config
from lib.TableGenerator import TableGenerator
from lib.helpers import generateAllPeriods
from models.Portfolio import Portfolio
import pandas as pd
import plotly.express as px
from weblib import sections

st.write('# Portfolio Tracker')

# INPUTS
[portfolio, currency] = sections.inputs()
st.divider()

config = Config(argparse.Namespace(portfolio=portfolio, currency=currency))
portfolio = Portfolio(config)

sections.key_metrics(portfolio, config, st)
sections.portfolio_bar(portfolio)

tabs = st.tabs([str(platform) for platform in portfolio.platforms])

periods = generateAllPeriods(datetime.date(2024, 1, 1), datetime.date.today())

for platform, tab in zip(portfolio.platforms, tabs):
    sections.key_metrics(platform, config, tab)
    sections.platform_metrics(platform, portfolio, tab)
    sections.platform_returns(platform, periods, tab)



# # Initialize an empty DataFrame to store results for all platforms
# all_platform_data = [] 

# # Loop over each platform in the portfolio
# for platform in portfolio.platforms:
#     df = pd.DataFrame(columns=["Date", "Value"])
    
#     for period in periods:
#         # Fill the period with the platform's valuations and transactions
#         period.fill(platform.valuations, platform.transactions)
        
#         # Prepare a new row for the DataFrame
#         new_row = pd.DataFrame({
#             "Date": [period.end],  # Date associated with the period
#             "Value": [float(period.calculateCurrentValue())]  # Calculated return value
#         })
        
#         # Concatenate the new row to the platform's DataFrame
#         df = pd.concat([df, new_row], ignore_index=True)
    
#     # Set the Date as the index and rename the 'Value' column with the platform's name
#     df.set_index("Date", inplace=True)
#     df.rename(columns={"Value": platform.__str__()}, inplace=True)
    
#     # Append the platform data to the list of all platform data
#     all_platform_data.append(df)

# # Combine all platform DataFrames into one DataFrame
# combined_df = pd.concat(all_platform_data, axis=1)

# # Display the combined DataFrame
# st.write(combined_df)

# # Plot the line chart for all platforms
# st.line_chart(combined_df)
