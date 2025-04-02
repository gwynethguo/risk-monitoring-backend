import asyncio
from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database import get_db
from app.routers import clients, margin, market_data, positions
from app.services.twelve_data_ws import start_twelve_data_connection
from app.ws.ws_handler import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_twelve_data_connection())

    yield

    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows the frontend from localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(clients.router, prefix="/api", tags=["clients"])
app.include_router(market_data.router, prefix="/api", tags=["market_data"])
app.include_router(positions.router, prefix="/api", tags=["positions"])
app.include_router(margin.router, prefix="/api", tags=["margin"])


@app.websocket("/ws/{client_id}")
async def websocket_route(websocket: WebSocket, client_id: int):
    await websocket_endpoint(websocket, client_id)
