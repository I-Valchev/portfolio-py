import pymongo
import streamlit as st
from lib.Entities.GroupEntities import PlatformEntity
from lib.Entities.Portfolio import PortfolioEntity
from lib.db.Models import DbPortfolio, DbTransaction, DbValuation
from typing import NamedTuple

class OperationResult(NamedTuple):
    success: bool
    message: str


class Database:
    def __init__(self):
        self.conn = self.__init_connection()
        self._ttl = '10m'

    # TODO: cache with @st.cache_data(ttl=1)
    def readPortfolios(self) -> list[PortfolioEntity]:
        dbPortfolios = self.conn.get_database("all_data").portfolios.find(limit=3)
        return [self.__parse_portfolio(item) for item in dbPortfolios]
    
    def fetchPortfolioByName(self, name: str) -> PortfolioEntity:
        dbPortfolio = self.conn.get_database("all_data").portfolios.find_one({"name": name})
        return self.__parse_portfolio(dbPortfolio) if dbPortfolio else None

    
    def fetchAllPortfolioNames(self) -> list[str]:
        # Query for all portfolios, returning only the 'name' field
        dbPortfolios = self.conn.get_database("all_data").portfolios.find(
            {},  # No filter, get all portfolios
            {"_id": 0, "name": 1}  # Projection to return only 'name' field
        )
        return [portfolio["name"] for portfolio in dbPortfolios]
    
    def add_new_platform(self, portfolio: PortfolioEntity, platform: PlatformEntity) -> OperationResult:
        result = self.conn.get_database("all_data").portfolios.update_one(
            {"name": portfolio.name},
            {"$push": {"platforms": platform._dbPlatform.model_dump()}}
        )

        if result.modified_count > 0:
            return OperationResult(True, f"Platform '{platform.pretty}' added successfully.")
        else:
            return OperationResult(False, f"Failed to add platform '{platform.pretty}'.")
    
    def save_platform_changes(self, portfolio_name: str, platform_name: str, new_valuations: list[DbValuation] = None, new_transactions: list[DbTransaction] = None) -> OperationResult:
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
                return OperationResult(True, f"Platform '{platform_name}' added successfully.")
            else:
                return OperationResult(False, f"Failed to add platform '{platform_name}'.")

    def __parse_portfolio(self, data: dict) -> PortfolioEntity:
        if data:
            # Convert ObjectId to string (since Pydantic doesn’t support ObjectId)
            data["id"] = str(data["_id"])  # Add 'id' field for Pydantic
            del data["_id"]  # Remove '_id' since it's not part of the Pydantic model

            # Create and return the Portfolio instance
            return PortfolioEntity(DbPortfolio(**data))
        return None

    # TODO: cache with @st.cache_resource
    def __init_connection(self):
        return pymongo.MongoClient(**st.secrets["mongo"])
