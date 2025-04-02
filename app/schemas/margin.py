from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional


# Response schema for getting client data
class MarginResponse(BaseModel):
    portfolio_market_value: float
    loan_amount: float
    net_equity: float
    total_margin_requirement: float
    margin_shortfall: float
