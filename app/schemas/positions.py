from pydantic import BaseModel
from typing import Optional


# Request schema for position creation
class PositionCreate(BaseModel):
    client_id: int
    symbol: str
    exchange: Optional[str] = None
    quantity: float

    class Config:
        from_attributes = True


# Response schema for returning position details
class PositionResponse(BaseModel):
    id: int
    client_id: int
    symbol: str
    exchange: Optional[str] = None
    quantity: float

    class Config:
        from_attributes = True
