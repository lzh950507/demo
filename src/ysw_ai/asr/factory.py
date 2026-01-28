import os

from ysw_ai.asr.base import ASRModel
from ysw_ai.asr.faster_whisper_model import FasterWhisperASRModel

from ysw_core.utils.config import settings

def getASRModel() -> ASRModel:
    if settings.asr.provider == "faster-whisper":
        config = {
            "model_size": settings.asr.faster_whisper.model_size,
            "device": settings.asr.faster_whisper.device,
            "compute_type": settings.asr.faster_whisper.compute_type,
        }
        return FasterWhisperASRModel(config)
    else:
        raise Exception(f"Unsupported provider: {settings.provider}")
