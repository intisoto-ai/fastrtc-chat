import numpy as np
from fastrtc_chat.translate import translate_text

def dummy_speech_to_text(audio):
    """Simulates speech-to-text (STT)."""
    return "Hello, how are you?"

def dummy_text_to_speech(text):
    """Simulates text-to-speech (TTS)."""
    return text  # In real case, return an audio file

def process_audio(audio: tuple[int, np.ndarray]):
    """
    Converts speech to text, translates, and converts back to speech.
    """
    input_text = dummy_speech_to_text(audio)
    translated_text = translate_text(input_text, "es")
    response_audio = dummy_text_to_speech(translated_text)
    return response_audio
