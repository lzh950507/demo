import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, Union, BinaryIO

import numpy as np
from faster_whisper import WhisperModel
from loguru import logger

from ysw_ai.asr.base import ASRModel, TranscriptionResult

executor = ThreadPoolExecutor(2, "faster-whisper-thread")


class FasterWhisperASRModel(ASRModel):
    def __init__(self, config: Dict[str, Any]):
        """
        FasterWhisper ASR 模型
        :param config:
                - model_size: 模型大小 ("tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3")
                - device: 设备 ("cpu", "cuda", "auto")
                - compute_type: 计算类型 ("float16", "float32", "int8", "int8_float16")
                - download_root: 模型下载路径
                - language: 默认语言
                - beam_size: beam search大小
                - vad_filter: 是否启用VAD过滤
                - temperature: 温度参数
        """
        super().__init__(config)
        self.model_size = config.get('model_size', "base")
        self.device = config.get('device', "auto")
        self.compute_type = config.get("compute_type", "float16")
        self.download_root = config.get("download_root")
        self.default_language = config.get("language", None)
        self.beam_size = config.get("beam_size", 5)
        self.vad_filter = config.get("vad_filter", False)
        self.temperature = config.get("temperature", 0)
        self.initial_prompt = config.get("initial_prompt", None)

        self.model: Optional[WhisperModel] = None

    def initialize(self) -> None:
        if self._initialized:
            return
        try:
            # 加载模型
            self.model = WhisperModel(
                model_size_or_path=self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=self.download_root,
                cpu_threads=8,
                local_files_only=False

            )
            self._initialized = True
            logger.info(f"Faster-Whisper model loaded successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Faster-Whisper: {e}")
            raise


    async def transcribe(
            self,
            audio_data: Union[str, BinaryIO, np.ndarray],
            language: Optional[str] = None,
            word_timestamps: bool = False,
            **kwargs
    ) -> TranscriptionResult:
        if not self._initialized:
            self.initialize()
        try:
            def _transcribe_sync():
                segments, info = self.model.transcribe(
                    audio_data,
                    language=language,
                    beam_size=self.beam_size,
                    word_timestamps=word_timestamps
                )
                # 收集所有片段 (this triggers the blocking inference)
                return list(segments), info

            loop = asyncio.get_running_loop()
            segments_list, info = await loop.run_in_executor(executor, _transcribe_sync)

            # 拼接文本
            full_text = " ".join([seg.text for seg in segments_list])

            # 准备分段信息
            segment_details = []
            for seg in segments_list:
                segment_details.append({
                    "text": seg.text,
                    "start": seg.start,
                    "end": seg.end,
                    "words": seg.words if hasattr(seg, 'words') else None,
                })
            return TranscriptionResult(
                text=full_text.strip(),
                language=info.language if info.language else (language or self.default_language),
                segments=segment_details
            )

        except Exception as e:
            logger.error(f"Faster-Whisper transcription failed: {e}")
            raise



