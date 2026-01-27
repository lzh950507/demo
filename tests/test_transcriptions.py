import asyncio

from dynaconf import Dynaconf

from ysw_core.utils.logger import setup_logging
from ysw_ai.asr import factory
from loguru import logger
setup_logging()


model = factory.getASRModel()

async def test():

    info = await model.transcribe("D:\\work_store\\WXWork\\1688857904683167\\Cache\\File\\2025-12\\mp3-1.wav", "en", True)

    logger.info(f"Transcription: {info}")


if __name__ == '__main__':
    asyncio.run(test())