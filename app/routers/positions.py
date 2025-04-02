from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.market_data import get_market_data, get_market_data_by_instrument
from app.schemas.positions import PositionCreate, PositionResponse

from app import crud
from app.database import get_db
from app.schemas.market_data import MarketDataResponse, MarketInstrument
from app.ws.ws_handler import send_position_update

router = APIRouter()


# Create a position
@router.post("/positions", response_model=PositionResponse)
async def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    db_position = crud.positions.get_position(
        db, client_id=position.client_id, symbol=position.symbol
    )
    if db_position:
        raise HTTPException(status_code=400, detail="Position already exists")
    return crud.positions.create_position(db=db, **position.model_dump())


# Get instruments
@router.get("/positions/instruments", response_model=list[MarketInstrument])
def get_instruments(db: Session = Depends(get_db)):
    return [MarketInstrument(**resp) for resp in crud.positions.get_instruments(db)]


# Get positions by client id
@router.get("/positions/client/{client_id}", response_model=list[PositionResponse])
def get_positions_by_client(client_id: int, db: Session = Depends(get_db)):
    return crud.positions.get_positions_by_client(db, client_id=client_id)


# Update a position
@router.put("/positions/{position_id}", response_model=PositionResponse)
def update_position(position_id: int, quantity: int, db: Session = Depends(get_db)):
    db_position = crud.positions.get_position_by_id(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return crud.positions.update_position(
        db=db, position_id=position_id, quantity=quantity
    )


# Delete a position
@router.delete("/positions/{position_id}", response_model=PositionResponse)
def delete_position(position_id: int, db: Session = Depends(get_db)):
    db_position = crud.positions.get_position_by_id(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return crud.positions.delete_position(db=db, position_id=position_id)
