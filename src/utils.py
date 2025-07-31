import asyncio
import os
from tempfile import NamedTemporaryFile


async def convert_wav_to_mp3(wav_file, mp3_path: str):
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        if hasattr(wav_file, "read"):
            contents = wav_file.read()
        elif hasattr(wav_file, "read"):
            contents = await wav_file.read()
        else:
            raise ValueError("Unsupported file object type")

        tmp_wav.write(contents)
        tmp_wav_path = tmp_wav.name

    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-i",
            tmp_wav_path,
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            mp3_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode()}")

        return True
    finally:
        if os.path.exists(tmp_wav_path):
            os.unlink(tmp_wav_path)
