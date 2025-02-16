
import pandas as pd
import streamlit as st
from lib.Entities.GroupEntities import PeriodEntity, PlatformEntity
from lib.Entities.Portfolio import PortfolioEntity
from lib.db.Database import Database
from lib.db.Models import DbTransaction, DbValuation
from lib.helpers import availablePortfolios


def inputs():
    col1, col2 = st.columns(2)

    portfolio = col1.selectbox('Portfolio', availablePortfolios())
    currency = col2.selectbox('Currency', ['EUR', 'BGN'])

    return [portfolio, currency]

def key_metrics(portfolio: PortfolioEntity | PlatformEntity, currency: str, target: st):
    col1, col2 = target.columns(2)

    delta = "{:.2f}".format(portfolio.calculateCurrentValue() - portfolio.calculateBalance())
    col1.metric(label='Portfolio Value', value=f"{portfolio.calculateCurrentValue()} {currency}", delta=f"{delta}")
    col2.metric(label='Unrealized Gain/Loss', value=f"{portfolio.unrealisedGainLoss()} %")

def portfolio_bar(portfolio: PortfolioEntity):
    # Extract names and balances
    platform_names = [str(platform) for platform in portfolio.platforms]
    platform_balances = [int(platform.calculateCurrentValue()) for platform in portfolio.platforms]
    # platform_colors = [config.config['platforms'][platform.name]['color'] for platform in portfolio.platforms]

    # Create a pandas DataFrame
    data = pd.DataFrame({
        "Platform": platform_names,
        "Value": platform_balances,
    })

    st.bar_chart(data, x='Platform', y='Value')

def platform_metrics(plaform: PlatformEntity, portfolio: PortfolioEntity, target: st):
    col1, col2 = target.columns(2)

    col1.metric(label='Portfolio Share', value=f"{plaform.calculatePortfolioShare(portfolio.calculateCurrentValue())} %")

def platform_returns(platform: PlatformEntity, periods: list[PeriodEntity], tab: st):
    df = pd.DataFrame(columns=["Period", "Return"])

    start_adding = False
    for period in periods:
        period.fill(platform.valuations, platform.transactions)
        return_value = period.calculateReturn()

        # Only add rows after the first non-zero return value
        if return_value != 0.0 or start_adding:

            new_row = pd.DataFrame({
                "Period": [period.start.strftime('%B %Y')],
                "Return": ["{:.2f}".format(return_value)]
            })

            df = pd.concat([df, new_row], ignore_index=True)
            
            start_adding = True
    tab.write("Monthly returns")
    tab.table(df)


def display_and_edit_objects(portfolio: PortfolioEntity, platform: PlatformEntity, objects, object_class, target: st):
    """Displays the objects in a Streamlit data editor and handles saving edits."""
    
    # Extract 'date' and 'value' from each object and build a DataFrame
    data = [(item.date, item.value) for item in objects]
    df = pd.DataFrame(data, columns=['date', 'value'])

    # Convert 'date' column to string format for easier editing
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')

    # Use a unique key for the data editor
    key = f"{portfolio.name}-{platform.name}-{object_class.__name__}"
    edited_df = target.data_editor(df, num_rows="dynamic", use_container_width=True, key=key)

    if target.button("Save", key=f"{key}-save"):
        # Convert 'date' back to datetime and build the list of the original objects
        edited_df['date'] = pd.to_datetime(edited_df['date'], format='%d-%m-%Y', errors='coerce')

        if object_class == DbValuation:
            Database().save_platform_changes(
                portfolio_name=portfolio.name,
                platform_name=platform.name,
                new_valuations=edited_df
            )
        elif object_class == DbTransaction:
            Database().save_platform_changes(
                portfolio_name=portfolio.name,
                platform_name=platform.name,
                new_transactions=edited_df
            )

        st.rerun()

def add_new_platform(portfolio: PortfolioEntity, target: st):
    target.write('## Add a new Platform')

    platform_name = target.text_input('Platform Name')

    if target.button("Create Platform"):
        if platform_name:
            new_platform = PlatformEntity.new(pretty=platform_name)
            result = Database().add_new_platform(portfolio, new_platform)
            st.rerun()
            if result:
                target.success(result.message)
            else:
                target.warning(result.message)

        else:
            target.warning("Please enter a platform name")