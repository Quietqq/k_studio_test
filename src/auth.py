from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import get_user_by_token
from src.database import get_async_session

api_key_header = APIKeyHeader(name="Token", auto_error=False)


async def verify_token(token: str, db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token")
    return user
