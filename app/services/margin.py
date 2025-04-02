from sqlalchemy.orm import Session
from app.logger import logger
from app.crud.market_data import get_market_data_by_instrument
from app.crud.positions import get_positions_by_client
from app.crud.clients import get_client
from app.schemas.margin import MarginResponse


def calculate_margin_status(db: Session, client_id: int):
    # Fetch positions and loan amount from the database
    positions = get_positions_by_client(db, client_id)
    loan_amount = get_client(db, client_id).loan

    # Calculate the portfolio market value
    portfolio_market_value = sum(
        position.quantity
        * get_market_data_by_instrument(db, position.symbol, position.exchange).price
        for position in positions
    )

    logger.info(f"{portfolio_market_value=} {loan_amount=}")

    # Calculate net equity
    net_equity = portfolio_market_value - loan_amount

    # Calculate total margin requirement (25% of the portfolio market value)
    maintenance_margin_rate = 0.25
    total_margin_requirement = maintenance_margin_rate * portfolio_market_value

    # Calculate margin shortfall
    margin_shortfall = total_margin_requirement - net_equity

    # Return the result
    return MarginResponse(
        portfolio_market_value=portfolio_market_value,
        loan_amount=loan_amount,
        net_equity=net_equity,
        total_margin_requirement=total_margin_requirement,
        margin_shortfall=margin_shortfall,
    )
