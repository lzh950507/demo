from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter(prefix="/home", tags=["home"])

@router.get("")
async def home():
    return {"message": "Hello World", "code": 0}