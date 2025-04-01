from sqlalchemy.orm import Session
from app.models import Position


def create_position(
    db: Session,
    client_id: int,
    symbol: str,
    exchange: str,
    quantity: float,
):
    position = Position(
        client_id=client_id, symbol=symbol, exchange=exchange, quantity=quantity
    )
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def get_instruments(db: Session):
    result = db.query(Position.symbol, Position.exchange).distinct().all()
    return [{"symbol": row[0], "exchange": row[1]} for row in result]


def get_position(db: Session, client_id: int, symbol: str):
    return (
        db.query(Position)
        .filter(Position.symbol == symbol)
        .filter(Position.client_id == client_id)
        .all()
    )


def get_position_by_id(db: Session, position_id: int):
    return db.query(Position).filter(Position.id == position_id).all()


def get_positions_by_client(db: Session, client_id: int):
    return db.query(Position).filter(Position.client_id == client_id).all()


def update_position(db: Session, position_id: int, quantity: int):
    position = db.query(Position).filter(Position.id == position_id).first()
    if position:
        position.quantity = quantity
        db.commit()
        db.refresh(position)
    return position


def delete_position(db: Session, position_id: int):
    position = db.query(Position).filter(Position.id == position_id).first()
    if position:
        db.delete(position)
        db.commit()
    return position
