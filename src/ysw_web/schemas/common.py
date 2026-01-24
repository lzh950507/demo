from pydantic import BaseModel


class CommonResult(BaseModel):
    code: int
    message: str
    data: dict

