import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, Form, Request
from fastapi import File

from ysw_ai.asr.factory import getASRModel
from ysw_web.utils.response import success

router = APIRouter()

asr_model = getASRModel()

@router.post("/recordAudioEvaluation")
async def record_audio_evaluation(
        file: UploadFile = File(...)
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