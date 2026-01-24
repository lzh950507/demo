from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

from ysw_core.utils.logger import setup_logging
from ysw_core.utils.config import settings
from ysw_web.utils.exception_handlers import register_exception_handlers
from ysw_web.routers import home
from ysw_web.routers import asr


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup logging using pathlib
    log_dir = settings.logging.file.path
    setup_logging(log_dir=log_dir)
    logger.info(f"env: {settings.current_env}")
    logger.info(f"Logging to {log_dir}")
    logger.info("Service Starting up")
    yield
    logger.info("Service Shutting down")


app = FastAPI(lifespan=lifespan)

# Register global exception handlers
register_exception_handlers(app)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(home.router)
app.include_router(asr.router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
