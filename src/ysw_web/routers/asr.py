from fastapi import APIRouter, File, UploadFile
from starlette.responses import HTMLResponse
from fastapi import File
from fastapi.responses import JSONResponse
import shutil
import os
from faster_whisper import WhisperModel
from loguru import logger

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
router = APIRouter(prefix="/asr", tags=["home"])

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    temp_file = f"temp_{file.filename}"
    
    # 保存上传的文件到临时文件
    with open(temp_file, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    try:
        # 使用 Whisper 模型进行转录
        segments, info = model.transcribe(temp_file, beam_size=5)
        # 组装转录结果
        # 组装转录结果
        results = [{
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        } for segment in segments]

        # 拼接完整文本
        full_text = "".join([item["text"] for item in results])
 
        return JSONResponse(content={
            "language": info.language,
            "language_probability": info.language_probability,
            "transcription": results,
            "full_text": full_text
        })
    finally:
        os.remove(temp_file)