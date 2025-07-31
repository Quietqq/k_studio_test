import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.orm_models.tables import AudioRecord, Users


async def create_user(db: AsyncSession, name: str) -> Users:
    res = await db.execute(select(Users).where(Users.name == name))

    if not res.scalar_one_or_none():
        user = Users(name=name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=409, detail="User already registered")


async def get_user_by_token(db: AsyncSession, token: str):

    res = await db.execute(select(Users).where(Users.token == token))
    return res.scalar_one_or_none()


async def create_audio_record(
    db: AsyncSession, user_id: uuid.UUID, original_filename: str, mp3_filename: str
) -> AudioRecord:
    record = AudioRecord(
        user_id=user_id, original_filename=original_filename, mp3_filename=mp3_filename
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record
