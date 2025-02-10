from pydantic import BaseModel
from datetime import datetime
from typing import List

from models.Valuation import Valuation
from models.Transaction import Transaction
from models.Platform import Platform
from models.Portfolio import Portfolio

class DbTransaction(BaseModel, Transaction):
    date: datetime
    value: float

class DbValuation(BaseModel, Valuation):
    date: datetime
    value: float

class DbPlatformModel(BaseModel, Platform):
    name: str
    pretty: str
    color: str
    transactions: List[DbTransaction] = []
    valuations: List[DbValuation] = []

    # TODO: clean this up
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        Platform.__init__(self)

    def __str__(self):
        return Platform.__str__(self)

class DbPortfolio(BaseModel, Portfolio):
    name: str
    currency: str
    platforms: List[DbPlatformModel]

def parse_portfolio(data):
    if data:
        # Convert ObjectId to string (since Pydantic doesn’t support ObjectId)
        data["id"] = str(data["_id"])  # Add 'id' field for Pydantic
        del data["_id"]  # Remove '_id' since it's not part of the Pydantic model

        # Create and return the Portfolio instance
        return DbPortfolio(**data)
    return None