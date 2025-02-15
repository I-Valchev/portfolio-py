from pydantic import BaseModel
from datetime import datetime
from typing import List

class DbTransaction(BaseModel):
    date: datetime
    value: float

class DbValuation(BaseModel):
    date: datetime
    value: float

class DbPlatform(BaseModel):
    name: str
    pretty: str
    color: str
    transactions: List[DbTransaction] = []
    valuations: List[DbValuation] = []

class DbPortfolio(BaseModel):
    name: str
    currency: str
    platforms: List[DbPlatform]
