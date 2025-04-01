from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.clients import ClientCreate, ClientResponse
from app import crud
from app.database import get_db
from app.logger import logger

router = APIRouter()


# Create a client
@router.post("/clients/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    logger.info(client.model_dump())
    return crud.clients.create_client(db=db, **client.model_dump())


# Get a single client by id
@router.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.clients.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client


# Update a client
@router.put("/clients/{client_id}", response_model=ClientResponse)
def update_client_loan(client_id: int, loan: int, db: Session = Depends(get_db)):
    db_client = crud.clients.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.clients.update_client_loan(db=db, client_id=client_id, loan=loan)


# Delete a client
@router.delete("/clients/{client_id}", response_model=ClientResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.clients.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.clients.delete_client(db=db, client_id=client_id)
