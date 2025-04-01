from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.logger import logger
from app.database import get_db
from app.services.margin import calculate_margin_shortfall

router = APIRouter()


# Get margin shortfall
@router.post("/margin-shortfall/{client_id}", response_model=None)
def get_margin_shortfall(client_id: int, db: Session = Depends(get_db)):
    return calculate_margin_shortfall(db=db, client_id=client_id)
