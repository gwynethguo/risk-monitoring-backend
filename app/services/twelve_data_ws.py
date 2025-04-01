import asyncio
from datetime import datetime, timezone
from fastapi import Depends
import websockets
import json
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.logger import logger
from app.models import MarketData
from app.ws.ws_handler import (
    send_to_frontend,
)  # Function to send data to frontend clients
from app.crud.positions import get_instruments
from app.crud.market_data import add_market_data

load_dotenv()

TWELVE_DATA_WEBSOCKET_URL = os.getenv("TWELVE_DATA_WEBSOCKET_URL")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")


# Function to connect to Twelve Data WebSocket and subscribe to symbols
async def connect_to_twelve_data():
    logger.info("Connecting to twelve data websocket")
    async with websockets.connect(
        f"{TWELVE_DATA_WEBSOCKET_URL}quotes/price?apikey={TWELVE_DATA_API_KEY}"
    ) as websocket:
        # Send subscription message to the Twelve Data WebSocket for a specific symbol (e.g., AAPL)
        with SessionLocal() as db:
            symbols = ",".join(
                [
                    (
                        f"{instr['symbol']}:{instr['exchange']}"
                        if instr["exchange"] != None
                        else f"{instr['symbol']}"
                    )
                    for instr in get_instruments(db)
                ]
            )
        logger.info(f"{symbols=}")
        subscribe_message = {"action": "subscribe", "params": {"symbols": symbols}}
        await websocket.send(json.dumps(subscribe_message))

        message = await websocket.recv()
        data = json.loads(message)

        logger.info(f"{data=}")

        if data.get("status") != "ok":
            logger.info("Failed to subscribe to Twelve Data Price Websocket")

        for instr in data.get("success") or []:
            logger.info(f"Successfuly subscribed for instrument {instr.get('symbol')}")

        for instr in data.get("fails") or []:
            logger.info(f"Failed to subscribe for instruments {instr.get('symbol')}")

        while True:
            # Receive data from Twelve Data WebSocket
            message = await websocket.recv()
            data = json.loads(message)

            logger.info(f"{data=}")

            # Add to database
            with SessionLocal() as db:
                inserted_market_data = add_market_data(
                    db,
                    symbol=data.get("symbol"),
                    exchange=data.get("exchange"),
                    price=data.get("price"),
                    # timestamp=datetime.fromtimestamp(
                    #     data.get("timestamp"), timezone.utc
                    # ),
                )
                logger.info(inserted_market_data)
            # Forward data to frontend clients
            # await send_to_frontend(data)


# Start the connection to Twelve Data WebSocket
async def start_twelve_data_connection():
    await connect_to_twelve_data()
