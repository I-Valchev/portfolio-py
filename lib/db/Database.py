import pymongo
import streamlit as st

from lib.db.Models import DbTransaction, DbValuation, parse_portfolio


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
    
    def save_platform_changes(self, portfolio_name: str, platform_name: str, new_valuations: list[DbValuation] = None, new_transactions: list[DbTransaction] = None):
        """Replace valuations or transactions for a specific platform within a portfolio in MongoDB."""
        updates = {}

        if new_valuations is not None:
            updates["platforms.$.valuations"] = new_valuations.to_dict(orient="records")


        if new_transactions is not None:
            updates["platforms.$.transactions"] = new_transactions.to_dict(orient="records")

        if updates:
            result = self.conn.get_database("all_data").portfolios.update_one(
                {
                    "name": portfolio_name,
                    "platforms.name": platform_name  # Match the correct platform within the portfolio
                },
                {
                    "$set": updates  # Replace valuations and/or transactions
                }
            )
            if result.modified_count > 0:
                st.success(f"Successfully updated {platform_name} in {portfolio_name}")
            else:
                st.info(f"No changes made to {platform_name} in {portfolio_name}")


        
    # TODO: cache with @st.cache_resource
    def __init_connection(self):
        return pymongo.MongoClient(**st.secrets["mongo"])
