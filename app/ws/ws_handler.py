from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio

from app.logger import logger

# List to store active WebSocket connections (frontend clients)
active_connections: List[WebSocket] = []


# FastAPI WebSocket endpoint to handle frontend clients
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection from the frontend client
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("Client disconnected")


# Function to send data to all connected frontend WebSocket clients
async def send_to_frontend(data: dict):
    for connection in active_connections:
        await connection.send_json(data)
