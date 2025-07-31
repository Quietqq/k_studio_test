import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import verify_token
from src.crud import create_audio_record, create_user
from src.database import get_async_session
from src.orm_models.tables import AudioRecord
from src.shemas import AudioResponse, UserCreate, UserResponse
from src.utils import convert_wav_to_mp3

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
async def register_user(
    user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    db_user = await create_user(db=db, name=user.name)
    return db_user


@router.post("/upload/", response_model=AudioResponse)
async def upload_audio(
    request: Request,
    user_id: uuid.UUID,
    file: UploadFile = File(...),
    token: str = Header(..., alias="Token"),
    db: AsyncSession = Depends(get_async_session),
):
    current_user = await verify_token(token, db)

    if str(current_user.id) != str(user_id):
        raise HTTPException(status_code=403, detail="User ID mismatch")

    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(400, detail="Only WAV files are accepted")

    os.makedirs("static/converted", exist_ok=True)

    mp3_filename = f"{uuid.uuid4()}.mp3"
    mp3_path = os.path.join("static/converted", mp3_filename)

    try:
        success = await convert_wav_to_mp3(file.file, mp3_path)
        if not success:
            raise HTTPException(500, detail="Audio conversion failed")

        record = await create_audio_record(
            db, current_user.id, file.filename, mp3_filename
        )

        base_url = str(request.base_url).rstrip("/")
        download_url = f"{base_url}/record?id={record.id}&user={user_id}"

        return {"download_url": download_url}

    except Exception as e:
        if os.path.exists(mp3_path):
            os.unlink(mp3_path)
        raise HTTPException(500, detail=str(e))


@router.get("/record")
async def download_audio(
    id: uuid.UUID = Query(..., description="UUID аудиозаписи"),
    user: uuid.UUID = Query(..., description="UUID пользователя"),
    db: AsyncSession = Depends(get_async_session),
):

    record = await db.execute(
        select(AudioRecord)
        .where(AudioRecord.id == id)
        .where(AudioRecord.user_id == user)
    )
    record = record.scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=404, detail="Audio record not found or access denied"
        )

    mp3_path = f"static/converted/{record.mp3_filename}"

    if not os.path.exists(mp3_path):
        raise HTTPException(status_code=410, detail="Audio file not found on server")
    
    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename=f"{record.id}.mp3", 
    )
