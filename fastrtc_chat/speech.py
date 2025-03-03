# fastrtc_chat/speech.py
import numpy as np
import logging
from fastrtc_chat.translate import translate_text
from fastrtc import get_stt_model
from fastrtc_chat.google_tts import google_text_to_speech

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


def speech_to_text(sample_rate, audio):
    """Simulates speech-to-text (STT)."""
    return stt_model.stt((sample_rate, audio))


def text_to_speech(text):
    """Simulates text-to-speech (TTS)."""
    for audio_chunk in google_text_to_speech(text):
        if audio_chunk is not None:
            yield audio_chunk
        else:
            yield None


def process_audio(audio: tuple[int, np.ndarray]):
    """
    Converts speech to text, translates, and converts back to speech.
    """
    try:

        # we unpack audio to sample_rate, audio
        sample_rate, audio = audio

        transcribed_text = speech_to_text(sample_rate, audio)
        log.info(f"Input text: {transcribed_text}")

        translated_text = translate_text(transcribed_text, "es")
        log.info(f"Translated text: {translated_text}")
        for audio_data in text_to_speech(translated_text):
            if audio_data is not None:
                #We don't send more the text
                yield audio_data
            else:
                log.error(f"Error getting audio chunk")
                yield None
    except Exception as e:
        log.error(f"Error during process audio: {e}")
        yield None
