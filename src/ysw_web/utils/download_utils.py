import os
import uuid
from urllib.parse import urlparse

import httpx
from fastapi import UploadFile
from starlette.exceptions import HTTPException


async def save_file(file: UploadFile) -> str:
    file_path = get_download_path(file.filename)
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path
    except httpx.HTTPError as e:
        # 确保删除临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise HTTPException(
            status_code=200,
            detail=f"无法下载URL内容: {str(e)}"
        )


async def download_file(url: str) -> str:
    file_name = get_file_name(url)
    file_path = get_download_path(file_name)
    try:
        # 下载音频文件
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                with open(file_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)

        # 使用 asr 模型进行转录
        return file_path
    except httpx.HTTPError as e:
        # 确保删除临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=200,
            detail=f"无法下载URL内容: {str(e)}"
        )

def get_file_name(url: str) -> str:
    return os.path.basename(urlparse(url).path)

def get_download_path(file_name: str) -> str:
    download_dir = 'temp_file'
    os.makedirs(download_dir, exist_ok=True)
    file_id = uuid.uuid4()
    temp_file = f"temp_{file_id}_${file_name}"
    return os.path.join(download_dir, temp_file)