import asyncio
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database import get_db
from app.routers import clients, margin, market_data, positions
from app.services.twelve_data_ws import start_twelve_data_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_twelve_data_connection())

    yield

    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)

app.include_router(clients.router, prefix="/api", tags=["clients"])
app.include_router(market_data.router, prefix="/api", tags=["market_data"])
app.include_router(positions.router, prefix="/api", tags=["positions"])
app.include_router(margin.router, prefix="/api", tags=["margin"])
