from fastapi import APIRouter
from sqlalchemy import select

from db.session import SessionDep
from core.token_utils import (
    create_token, 
    validate_token, 
    delete_tokens)
from schemas.types_schema import (
    CreateTokens,
    ValidateTokens,
    DeleteTokens
    )
from schemas.validate_schema import Valid
from db.models import Token


router = APIRouter(prefix="/app", tags=["Выдача токена"])


@router.get('/tokens')
async def get_all_tokens(db: SessionDep):
    tokens = await db.execute(select(Token))
    return tokens.scalars().all()


@router.post('/token', response_model=CreateTokens)
async def create_tokens(db: SessionDep):
    token = await create_token(db=db)
    return {
        "status_code": 200,
        "token": token
    }

@router.post("/valid/{token}", response_model=ValidateTokens)
async def validate_tokens(param: Valid, db: SessionDep):
    is_valid = await validate_token(token_value=param.token, db=db)
    return {
        "status_code": 200,
        "status": is_valid
    }

@router.delete("/clear/all/tokens", response_model=DeleteTokens)
async def delete_token(db:SessionDep):
    await delete_tokens(db=db)
    return {
        "status_code": 200,
        "status": True
    }
    