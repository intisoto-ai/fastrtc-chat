# fastrtc_chat/speech.py
import numpy as np
import logging
from fastrtc_chat.translate import translate_text
from fastrtc import get_stt_model, get_tts_model

log = logging.getLogger(__name__)
# Configure logging
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# Initialize models
try:
    stt_model = get_stt_model()
except Exception as e:
    log.error(f"Error initializing STT model: {e}")
    exit()

try:
    tts_model = get_tts_model()
except Exception as e:
    log.error(f"Error initializing TTS model: {e}")
    exit()

def dummy_speech_to_text(audio):
    """Simulates speech-to-text (STT)."""
    return stt_model.stt(audio)


def dummy_text_to_speech(text):
    """Simulates text-to-speech (TTS)."""
    for audio_chunk in tts_model.stream_tts_sync(text):
        yield audio_chunk


def process_audio(audio: tuple[int, np.ndarray]):
    """
    Converts speech to text, translates, and converts back to speech.
    """
    try:
        input_text = dummy_speech_to_text(audio)
        log.info(f"Input text: {input_text}")
        translated_text = translate_text(input_text, "es")
        log.info(f"Translated text: {translated_text}")
        for audio_chunk in dummy_text_to_speech(translated_text):
            yield audio_chunk
    except Exception as e:
        log.error(f"Error during process audio: {e}")
        yield None

