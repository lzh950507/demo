from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union, BinaryIO

import numpy as np


@dataclass
class TranscriptionResult:
    """
    转录结果
    """
    text: str
    language: Optional[str] = None
    segments: Optional[List[Dict]] = None
    words: Optional[List[Dict]] = None

class ASRModel:
    """
    ASR 抽象基类
    """
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """初始化模型（异步）"""
        pass

    @abstractmethod
    async def transcribe(
            self,
            audio_data: Union[str, BinaryIO, np.ndarray],
            language: Optional[str] = None,
            word_timestamps: bool = False,
            **kwargs
    ) -> TranscriptionResult:
        """
        转录音频

        Args:
            audio_data: 音频数据（字节流或文件路径）
            audio_format: 音频格式
            sample_rate: 采样率
            language: 语言代码（如 'zh-CN', 'en-US'）
            **kwargs: 额外参数

        Returns:
            TranscriptionResult: 转录结果
        """
        pass