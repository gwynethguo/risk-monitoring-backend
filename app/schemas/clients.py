from pydantic import BaseModel
from typing import Optional


# Request schema for creating a new client
class ClientCreate(BaseModel):
    name: str
    loan: float

    class Config:
        from_attributes = True


# Response schema for getting client data
class ClientResponse(BaseModel):
    id: int
    name: str
    loan: float

    class Config:
        from_attributes = True
