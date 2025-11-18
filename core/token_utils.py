import secrets
from datetime import datetime, timedelta
from client.config.config import Config
from db.models import Token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

def generate_token() -> str:
    prefix = secrets.randbelow(999999)
    body = secrets.token_urlsafe(8)[:Config.token_length]
    return f"{prefix}:{body}"

async def create_token(db: AsyncSession, ttl_minutes: int = 60):
    value = generate_token()
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    
    token = Token(token =  value, expires_at = expires_at)
    db.add(token)
    await db.commit()
    return value

async def validate_token(db: AsyncSession, token_value: str) -> bool:
    get_token = await db.execute(select(Token).where(Token.token == token_value))
    result = get_token.scalar_one_or_none()
    if not result:
        return False
    if result.expires_at < datetime.utcnow():
        await db.delete(result)
        await db.commit()
        return False
    return True 

async def delete_tokens(db: AsyncSession):
    await db.execute(delete(Token).where(Token.expires_at < datetime.utcnow()))
    await db.commit()
    
    