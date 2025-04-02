# app/ws/manager.py
from typing import Dict, Set
import asyncio

from fastapi import WebSocket

from app.logger import logger
from app.crud.positions import get_instruments_by_client
from app.database import SessionLocal
from app.routers.market_data import get_market_data
from app.services.margin import calculate_margin_status


class ConnectionManager:
    def __init__(self):
        # Tracks all active WebSocket connections by client_id
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str):
        async with self.lock:
            await websocket.accept()
            if client_id not in self.active_connections:
                self.active_connections[client_id] = set()
            self.active_connections[client_id].add(websocket)
            print(
                f"New connection for {client_id}. Total sessions: {len(self.active_connections[client_id])}"
            )

    async def disconnect(self, websocket: WebSocket, client_id: str):
        async with self.lock:
            if client_id in self.active_connections:
                self.active_connections[client_id].discard(websocket)

                # Only remove client_id if no more connections exist
                if not self.active_connections[client_id]:
                    del self.active_connections[client_id]
                    print(f"All connections closed for {client_id}")
                else:
                    print(
                        f"One connection closed for {client_id}. Remaining: {len(self.active_connections[client_id])}"
                    )

    async def send_to_clients(self, message: dict):
        async with self.lock:
            for client_id, ws_set in self.active_connections.items():
                with SessionLocal() as db:
                    if {
                        "symbol": message["symbol"],
                        "exchange": message["exchange"],
                    } in get_instruments_by_client(db, client_id):
                        market_data = get_market_data(client_id, db)
                        margin_status = calculate_margin_status(db, client_id)
                        margin_status_dict = margin_status.model_dump()
                        margin_status_dict["event"] = "margin"
                        logger.info(f"{message=}")
                        for ws in list(ws_set):
                            try:
                                for data in market_data:
                                    data["event"] = "price"
                                    await ws.send_json(data)
                                await ws.send_json(margin_status_dict)
                            except:
                                await self.disconnect(ws, client_id)

    async def send_to_client(self, message: dict, client_id: str):
        async with self.lock:
            if client_id in self.active_connections:
                for ws in list(self.active_connections[client_id]):  # Create copy
                    try:
                        await ws.send_json(message)
                    except:
                        await self.disconnect(ws, client_id)
