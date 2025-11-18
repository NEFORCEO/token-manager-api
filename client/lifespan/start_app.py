from contextlib import asynccontextmanager
from log.log import logger
from fastapi import FastAPI
from db.session import init_db


@asynccontextmanager
async def start_app(app: FastAPI):
    logger.info("START APP")
    await init_db()
    yield
    logger.info("APP CLOSE")