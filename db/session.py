from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from client.config.config import Config as con
from db.base import Base

engine = create_async_engine(url=con.url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_session():
    async with async_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]