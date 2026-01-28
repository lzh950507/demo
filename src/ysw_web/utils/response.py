from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def create(code: int = 0, message: str = "success", data: dict = None) -> dict:
    content = {"code": code, "msg": message, "data": data}
    return JSONResponse(content = jsonable_encoder(content))


def success(data: dict = None) -> dict:
    return create(data = data)

def error(code: int = 999, message: str = "error") -> dict:
    return create(code, message, data)


