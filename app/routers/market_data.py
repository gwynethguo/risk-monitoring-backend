from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.crud.positions import get_positions_by_client
from app.schemas.market_data import MarketDataCreate, MarketDataResponse
from app import crud
from app.logger import logger
from app.database import get_db

router = APIRouter()


# Helper function
def get_symbol_exchange_from_instrument(instrument: str):
    if ":" in instrument:
        return instrument.split(":")
    return instrument, None


# Get market data
@router.get("/market-data/all", response_model=list[MarketDataResponse])
def get_market_data(db: Session = Depends(get_db)):
    return crud.market_data.get_market_data(db)


# Get market data by client id
@router.get("/market-data/client/{client_id}", response_model=list)
def get_market_data(client_id: int, db: Session = Depends(get_db)):
    instruments = crud.positions.get_instruments_by_client(db, client_id)
    logger.info(instruments)
    market_data = crud.market_data.get_market_data_by_instruments(db, instruments)
    positions = get_positions_by_client(db, client_id)
    position_map = {f"{p.symbol}:{p.exchange}": p for p in positions}
    market_data_map = {f"{p.symbol}:{p.exchange}": p for p in market_data}
    return [
        {
            "id": market_data_map[instrument].id,
            "symbol": position_map[instrument].symbol,
            "exchange": position_map[instrument].exchange,
            "quantity": position_map[instrument].quantity,
            "price": market_data_map[instrument].price,
        }
        for instrument in position_map.keys()
        if instrument in market_data_map
    ]


# Get market history
@router.get("/market-history/all", response_model=list[MarketDataResponse])
def get_market_history(db: Session = Depends(get_db)):
    return crud.market_data.get_market_history(db)


# Get market data by instrument
@router.get("/market-data/instrument", response_model=MarketDataResponse)
def get_market_data_by_instrument(instrument: str, db: Session = Depends(get_db)):
    symbol, exchange = get_symbol_exchange_from_instrument(instrument)
    logger.info(f"{symbol=} {exchange=}")
    db_market_data = crud.market_data.get_market_data_by_instrument(
        db, symbol=symbol, exchange=exchange
    )
    if db_market_data is None:
        raise HTTPException(status_code=404, detail="Market data not found")
    return db_market_data


# Get market data history by instrument
@router.get("/market-history/instrument", response_model=list[MarketDataResponse])
def get_market_history_by_instrument(instrument: str, db: Session = Depends(get_db)):
    symbol, exchange = get_symbol_exchange_from_instrument(instrument)
    db_market_data = crud.market_data.get_market_history_by_instrument(
        db, symbol=symbol, exchange=exchange
    )
    if db_market_data is None:
        raise HTTPException(status_code=404, detail="Market data not found")
    return db_market_data
