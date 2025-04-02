from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.logger import logger
from app.database import get_db
from app.schemas.margin import MarginResponse
from app.services.margin import calculate_margin_status

router = APIRouter()


# Get margin status
@router.get("/margin-status/{client_id}", response_model=MarginResponse)
def get_margin_status(client_id: int, db: Session = Depends(get_db)):
    return calculate_margin_status(db=db, client_id=client_id)
