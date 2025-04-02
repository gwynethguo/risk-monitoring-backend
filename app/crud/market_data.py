from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_, tuple_
from app.logger import logger
from app.models import MarketData
from app.schemas.market_data import MarketInstrument


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
            and_(
                MarketData.symbol == latest_timestamp_subquery.c.symbol,
                or_(
                    MarketData.exchange == latest_timestamp_subquery.c.exchange,
                    MarketData.exchange.is_(None)
                    & latest_timestamp_subquery.c.exchange.is_(None),
                ),
                MarketData.timestamp == latest_timestamp_subquery.c.timestamp,
            ),
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


def get_market_data_by_instruments(db: Session, instruments: list[map]):
    instrument_tuples = [(item["symbol"], item["exchange"]) for item in instruments]

    conditions = []
    for symbol, exchange in instrument_tuples:
        if exchange is None:
            conditions.append(
                (MarketData.symbol == symbol) & (MarketData.exchange.is_(None))
            )
        else:
            conditions.append(
                (MarketData.symbol == symbol) & (MarketData.exchange == exchange)
            )

    logger.info(instrument_tuples)
    latest_timestamp_subquery = (
        db.query(
            MarketData.symbol,
            MarketData.exchange,
            func.max(MarketData.timestamp).label("timestamp"),
        )
        .filter(or_(*conditions))
        .group_by(MarketData.symbol, MarketData.exchange)
        .subquery()
    )

    logger.info(f"{str(latest_timestamp_subquery)=}")

    return (
        db.query(MarketData)
        .join(
            latest_timestamp_subquery,
            and_(
                MarketData.symbol == latest_timestamp_subquery.c.symbol,
                or_(
                    MarketData.exchange == latest_timestamp_subquery.c.exchange,
                    MarketData.exchange.is_(None)
                    & latest_timestamp_subquery.c.exchange.is_(None),
                ),
                MarketData.timestamp == latest_timestamp_subquery.c.timestamp,
            ),
        )
        .all()
    )


def get_market_history_by_instrument(db: Session, symbol: str, exchange: str):
    return (
        db.query(MarketData)
        .filter(MarketData.symbol == symbol)
        .filter(MarketData.exchange == exchange)
        .order_by(MarketData.timestamp.asc())
        .all()
    )
