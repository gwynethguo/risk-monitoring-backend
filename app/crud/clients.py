from sqlalchemy.orm import Session
from app.models import Client


def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()


def create_client(db: Session, name: str, loan: str):
    client = Client(name=name, loan=loan)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client


def update_client_loan(db: Session, client_id: int, loan: float):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        client.loan = loan
        db.commit()
        db.refresh(client)
    return client
