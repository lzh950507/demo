from dataclasses import dataclass
from typing import Optional, List, Dict

from ysw_ai.asr import factory
from ysw_web.routers.asr import asr_model

asr_model = factory.getASRModel()

@dataclass
class RecordAudioEvaluationResult:
    """
    转录结果
    """
    text: str
    language: Optional[str] = None
    segments: Optional[List[Dict]] = None

async def record_audio_evaluation(
        real_text: str,
        file: str
) -> RecordAudioEvaluationResult:
    transcribe = asr_model.transcribe(file)
    pass


def matchSampleAndRecordedWords(self, real_text, recorded_transcript):
    words_estimated = recorded_transcript.split()

    if real_text is None:
        words_real = self.current_transcript[0].split()
    else:
        words_real = real_text.split()

    mapped_words, mapped_words_indices = wm.get_best_mapped_words(
        words_estimated, words_real)

    real_and_transcribed_words = []
    real_and_transcribed_words_ipa = []
    for word_idx in range(len(words_real)):
        if word_idx >= len(mapped_words)-1:
            mapped_words.append('-')
        real_and_transcribed_words.append(
            (words_real[word_idx],    mapped_words[word_idx]))
        real_and_transcribed_words_ipa.append((self.ipa_converter.convertToPhonem(words_real[word_idx]),
                                               self.ipa_converter.convertToPhonem(mapped_words[word_idx])))
    return real_and_transcribed_words, real_and_transcribed_words_ipa, mapped_words_indices
