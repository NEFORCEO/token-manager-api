from fastapi import APIRouter

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


router = APIRouter(prefix="/app", tags=["Выдача токена"])

@router.post('/token', response_model=CreateTokens)
async def create_tokens(db: SessionDep):
    token = await create_token(db=db)
    return {
        "status_code": 200,
        "token": token
    }

@router.get("/valid/{token}", response_model=ValidateTokens)
async def validate_tokens(token: str, db: SessionDep):
    is_valid = await validate_token(token_value=token, db=db)
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
    