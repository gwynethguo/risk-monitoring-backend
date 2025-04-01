from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from app.database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    loan = Column(Float, nullable=False)


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    symbol = Column(String, nullable=False)
    exchange = Column(String, nullable=True)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class MarketData(Base):
    __tablename__ = "market_data"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    exchange = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())
