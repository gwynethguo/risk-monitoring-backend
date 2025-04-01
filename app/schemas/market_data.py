from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Request schema for market data creation
class MarketDataCreate(BaseModel):
    symbol: str
    exchange: str
    price: float

    class Config:
        from_attributes = True


# Response schema for returning market data
class MarketDataResponse(BaseModel):
    id: int
    symbol: str
    exchange: str
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True


class MarketInstrument(BaseModel):
    symbol: str
    exchange: Optional[str]

    class Config:
        from_attributes = True
