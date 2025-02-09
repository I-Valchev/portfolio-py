from streamlit_gsheets import GSheetsConnection
import streamlit as st


class Database:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        self._ttl = '10m'

    def readPortfolios(self):
        return self.conn.read(worksheet= 'portfolios',ttl=self._ttl)

    def readPlatforms(self, portfolio: str):
        df = self.conn.read(worksheet='platforms', ttl=self._ttl)
        return df.loc[df['portfolio'] == portfolio]

    def readTransactions(self, portfolio: str, platform: str):
        df = self.conn.read(worksheet='transactions', ttl=self._ttl)
        return df.loc[(df['platform'] == platform) & (df['portfolio'] == portfolio)]
