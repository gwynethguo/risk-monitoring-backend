from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio

from app.crud.positions import get_instruments_by_client
from app.database import SessionLocal
from app.logger import logger
from app.models import Position
from app.ws.manager import ConnectionManager

manager = ConnectionManager()


# FastAPI WebSocket endpoint to handle frontend clients
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    logger.info(f"{client_id} connected")
    try:
        while True:
            # Keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_id)


# Function to send data to all connected frontend WebSocket clients
async def send_market_update(data: dict):
    logger.info(f"{data=}")
    await manager.send_to_clients(data)


async def send_position_update(update_data: dict):
    # modify data event to position
    update_data["event"] = "position"
    logger.info(f"{update_data=}")

    await manager.send_to_client(update_data, update_data["client_id"])
