import uuid
from typing import BinaryIO, List, Annotated, Literal
from fastapi import APIRouter, File, UploadFile, Form, Request
from starlette.responses import HTMLResponse
from fastapi import File
from fastapi.responses import JSONResponse
import shutil
import os
from faster_whisper import WhisperModel
from loguru import logger
from ysw_web.utils.response import success

from ysw_ai.asr.factory import getASRModel


router = APIRouter()

asr_model = getASRModel()

TimestampGranularities = list[Literal["segment", "word"]]

@router.post("/audio/transcriptions")
async def transcriptions(
        request: Request,
        file: UploadFile = File(...),
        timestamp_granularities: Annotated[
            TimestampGranularities,
            Form(alias="timestamp_granularities[]"),
        ] = ["segment"],
):
    file_id = uuid.uuid4()
    temp_file = f"temp_{file_id}_{file.filename}"
    try:
        # 保存上传的文件到临时文件
        with open(temp_file, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 使用 asr 模型进行转录
        info = await asr_model.transcribe(temp_file, word_timestamps = "word" in timestamp_granularities)
        return success(info)
    finally:
        os.remove(temp_file)