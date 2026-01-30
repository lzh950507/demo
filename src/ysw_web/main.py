from contextlib import asynccontextmanager

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from ysw_core.utils.config import settings
from ysw_core.utils.logger import setup_logging
from ysw_web.routers import asr
from ysw_web.routers import home
from ysw_web.utils.exception_handlers import register_exception_handlers

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Setup logging using pathlib
    setup_logging()
    logger.info(f"env: {settings.current_env}")
    logger.info("Service Starting up")

    # Eagerly initialize ASR model
    logger.info("Initializing ASR model...")
    asr.asr_model.initialize()
    logger.info("ASR model initialized.")
    
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
    uvicorn.run("main:app", host="0.0.0.0", port=48180, reload=True, log_config=None)
