from typing import Optional, List
import os
from fastapi import APIRouter, UploadFile, Form, Request
from fastapi import File
from ysw_ai.asr.factory import getASRModel
from ysw_web.utils.download_utils import download_file, save_file
from ysw_web.utils.response import success

router = APIRouter()

asr_model = getASRModel()

@router.post("/audio/transcriptions")
async def transcriptions(
        request: Request,
        file: Optional[UploadFile] = File(None),
        file_url: Optional[str] = Form(None),
        language: Optional[str] = Form('en'),
        timestamp_granularities: List[str] = Form(default=["segment"])
):

    if not file and not file_url:
        raise HTTPException(
            status_code=400,
            detail="必须提供文件上传或URL参数"
        )
    temp_file = None
    try:
        if file:
            temp_file = await save_file(file)
        elif file_url:
            temp_file = await download_file(file_url)
        # 使用 asr 模型进行转录
        info = await asr_model.transcribe(temp_file, language=language, word_timestamps = "word" in timestamp_granularities)
        return success(info)
    finally:
        if temp_file:
            os.remove(temp_file)
