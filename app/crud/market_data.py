from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import MarketData


def add_market_data(
    db: Session,
    symbol: str,
    exchange: str,
    price: int,
    # timestamp: datetime
):
    market_data = MarketData(
        symbol=symbol,
        exchange=exchange,
        price=price,
        # timestamp=timestamp,
    )
    db.add(market_data)
    db.commit()
    db.refresh(market_data)
    return market_data


def get_market_data(db: Session):
    latest_timestamp_subquery = (
        db.query(
            MarketData.symbol,
            MarketData.exchange,
            func.max(MarketData.timestamp).label("timestamp"),
        )
        .group_by(MarketData.symbol, MarketData.exchange)
        .subquery()
    )

    return (
        db.query(MarketData)
        .join(
            latest_timestamp_subquery,
            (MarketData.symbol == latest_timestamp_subquery.c.symbol)
            & (MarketData.exchange == latest_timestamp_subquery.c.exchange)
            & (MarketData.timestamp == latest_timestamp_subquery.c.timestamp),
        )
        .all()
    )


def get_market_history(db: Session):
    return db.query(MarketData).order_by(MarketData.timestamp.desc()).all()


def get_market_data_by_instrument(db: Session, symbol: str, exchange: str):
    return (
        db.query(MarketData)
        .filter(MarketData.symbol == symbol)
        .filter(MarketData.exchange == exchange)
        .order_by(MarketData.timestamp.desc())
        .first()
    )


def get_market_history_by_instrument(db: Session, symbol: str, exchange: str):
    return (
        db.query(MarketData)
        .filter(MarketData.symbol == symbol)
        .filter(MarketData.exchange == exchange)
        .order_by(MarketData.timestamp.asc())
        .all()
    )
