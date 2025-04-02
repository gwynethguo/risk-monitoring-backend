import websockets
import json
import os
import requests
from dotenv import load_dotenv
from app.database import SessionLocal
from app.logger import logger
from app.ws.ws_handler import send_market_update
from app.crud.positions import get_instruments
from app.crud.market_data import add_market_data
from app.routers.market_data import get_market_data

load_dotenv()

TWELVE_DATA_API_URL = os.getenv("TWELVE_DATA_API_URL")
TWELVE_DATA_WEBSOCKET_URL = os.getenv("TWELVE_DATA_WEBSOCKET_URL")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")


def get_symbols():
    with SessionLocal() as db:
        instruments_list = get_instruments(db)
        logger.info(f"{instruments_list=}")
        for instrument in instruments_list:
            symbol, exchange = instrument.values()
            response = requests.get(
                f"{TWELVE_DATA_API_URL}price?symbol={symbol}{f'&exchange={exchange}' if exchange != None else ''}&apikey={TWELVE_DATA_API_KEY}"
            )
            logger.info(f"{response.text=}")
            response.raise_for_status()
            data = response.json()
            inserted_market_data = add_market_data(
                db,
                symbol=symbol,
                exchange=exchange,
                price=data.get("price"),
            )
            logger.info(inserted_market_data)

        return [(mp["symbol"], mp["exchange"]) for mp in instruments_list], ",".join(
            [
                (
                    f"{instr['symbol']}:{instr['exchange']}"
                    if instr["exchange"] != None
                    else f"{instr['symbol']}"
                )
                for instr in instruments_list
            ]
        )


# Function to connect to Twelve Data WebSocket and subscribe to symbols
async def connect_to_twelve_data():
    logger.info("Connecting to twelve data websocket")
    async with websockets.connect(
        f"{TWELVE_DATA_WEBSOCKET_URL}quotes/price?apikey={TWELVE_DATA_API_KEY}"
    ) as websocket:
        instruments_list, symbols = get_symbols()
        subscribe_message = {
            "action": "subscribe",
            "params": {"symbols": symbols},
        }
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
            # Forward data to frontend clients
            frontend_data = {
                key: data[key]
                for key in data
                if key in ["event", "symbol", "exchange", "price"]
            }

            if "exchange" not in frontend_data:
                frontend_data["exchange"] = None

            await send_market_update(frontend_data)

            with SessionLocal() as db:
                next_instruments_list = [
                    (mp["symbol"], mp["exchange"]) for mp in get_instruments(db)
                ]
            diff_instruments_list = list(
                set(next_instruments_list) - set(instruments_list)
            )
            logger.info(f"{diff_instruments_list=}")
            if len(diff_instruments_list) > 0:
                for symbol, exchange in diff_instruments_list:
                    response = requests.get(
                        f"{TWELVE_DATA_API_URL}price?symbol={symbol}{f'&exchange={exchange}' if exchange != None else ''}&apikey={TWELVE_DATA_API_KEY}"
                    )
                    logger.info(f"{response.text=}")
                    response.raise_for_status()
                    data = response.json()
                    inserted_market_data = add_market_data(
                        db,
                        symbol=symbol,
                        exchange=exchange,
                        price=data.get("price"),
                    )
                    logger.info(inserted_market_data)
                subscribe_message = {
                    "action": "subscribe",
                    "params": {
                        "symbols": ",".join(
                            [
                                (
                                    f"{instr[0]}:{instr[1]}"
                                    if instr[1] != None
                                    else f"{instr[0]}"
                                )
                                for instr in diff_instruments_list
                            ]
                        )
                    },
                }
                await websocket.send(json.dumps(subscribe_message))
                instruments_list = next_instruments_list


# Start the connection to Twelve Data WebSocket
async def start_twelve_data_connection():
    await connect_to_twelve_data()
