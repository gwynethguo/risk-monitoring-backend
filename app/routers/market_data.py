from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.market_data import MarketDataCreate, MarketDataResponse
from app import crud
from app.database import get_db

router = APIRouter()


# Helper function
def get_symbol_exchange_from_instrument(instrument: str):
    if ":" in instrument:
        return instrument.split(":")
    return instrument, None


# Get market data
@router.get("/market-data", response_model=list[MarketDataResponse])
def get_market_data(db: Session = Depends(get_db)):
    return crud.market_data.get_market_data(db)


# Get market history
@router.get("/market-history", response_model=list[MarketDataResponse])
def get_market_history(db: Session = Depends(get_db)):
    return crud.market_data.get_market_history(db)


# Get market data by instrument
@router.get("/market-data/{instrument}", response_model=MarketDataResponse)
def get_market_data_by_instrument(instrument: str, db: Session = Depends(get_db)):
    symbol, exchange = get_symbol_exchange_from_instrument(instrument)
    db_market_data = crud.market_data.get_market_data_by_instrument(
        db, symbol=symbol, exchange=exchange
    )
    if db_market_data is None:
        raise HTTPException(status_code=404, detail="Market data not found")
    return db_market_data


# Get market data history by instrument
@router.get("/market-history/{instrument}", response_model=list[MarketDataResponse])
def get_market_history_by_instrument(instrument: str, db: Session = Depends(get_db)):
    symbol, exchange = get_symbol_exchange_from_instrument(instrument)
    db_market_data = crud.market_data.get_market_history_by_instrument(
        db, symbol=symbol, exchange=exchange
    )
    if db_market_data is None:
        raise HTTPException(status_code=404, detail="Market data not found")
    return db_market_data
