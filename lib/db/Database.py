import pymongo
from streamlit_gsheets import GSheetsConnection
import streamlit as st

from lib.db.Models import parse_portfolio


class Database:
    def __init__(self):
        self.conn = self.__init_connection()
        self._ttl = '10m'

    # TODO: cache with @st.cache_data(ttl=1)
    def readPortfolios(self):
        dbPortfolios = self.conn.get_database("all_data").portfolios.find(limit=3)
        return [parse_portfolio(item) for item in dbPortfolios]
    
    def fetchPortfolioByName(self, name: str):
        dbPortfolio = self.conn.get_database("all_data").portfolios.find_one({"name": name})
        if dbPortfolio:
            return parse_portfolio(dbPortfolio)
        return None 

    
    def fetchAllPortfolioNames(self):
        # Query for all portfolios, returning only the 'name' field
        dbPortfolios = self.conn.get_database("all_data").portfolios.find(
            {},  # No filter, get all portfolios
            {"_id": 0, "name": 1}  # Projection to return only 'name' field
        )
        return [portfolio["name"] for portfolio in dbPortfolios]

        
    # TODO: cache with @st.cache_resource
    def __init_connection(self):
        return pymongo.MongoClient(**st.secrets["mongo"])
