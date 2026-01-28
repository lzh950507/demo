from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette import status
from loguru import logger


async def http_exception_handler(request: Request, ex: StarletteHTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "code": ex.status_code,
            "msg": ex.detail,
            "data": None
        }
    )


async def validation_exception_handler(request: Request, ex: RequestValidationError):

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "msg": "参数校验错误",
            "data": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.error("系统异常", exc)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "msg": "服务内部错误",
            "data": None
        }
    )


def register_exception_handlers(app: FastAPI):
    """
    注册全局异常处理
    :param app
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
