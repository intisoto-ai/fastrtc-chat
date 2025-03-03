# fastrtc_chat/google_tts.py
import logging
from google.cloud import texttospeech_v1 as texttospeech
import os
import numpy as np

log = logging.getLogger(__name__)
# Configure logging
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def create_google_tts_client(credentials_path=None):
    """Creates a Google Text-to-Speech client, optionally using a service account file."""
    if credentials_path:
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            return texttospeech.TextToSpeechClient()
        except Exception as e:
            log.error(f"Error loading credentials from {credentials_path}: {e}")
            return None
    else:
        try:
            return texttospeech.TextToSpeechClient()
        except Exception as e:
            log.error(f"Error creating client: {e}")
            return None

# Initialize Google Cloud TTS API
credentials_path = os.environ.get("GOOGLE_FASTRTC_KEY")
if credentials_path is None:
    log.error("Error: Environment variable GOOGLE_FASTRTC_KEY is not set")
    exit()

google_tts_client = create_google_tts_client(credentials_path)
if google_tts_client is None:
    log.error("Failed to initialize Google TTS client. Check your credentials.")
    exit()

def google_text_to_speech(text, language_code="es-US", voice_name="es-US-Polyglot-1", speaking_rate=1.0, pitch=0.0):
    """Converts text to audio using Google Cloud Text-to-Speech."""
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Select the voice
        if voice_name:
            voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
        else:
            voice = texttospeech.VoiceSelectionParams(language_code=language_code)

        sample_rate = 16000
        # Select the audio file type
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16, 
            speaking_rate=speaking_rate, 
            pitch=pitch,
            sample_rate_hertz=sample_rate #Corrected line
        )

        # Perform the text-to-speech request
        response = google_tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        if response.audio_content:

            audio = np.frombuffer(response.audio_content, dtype=np.int16)
            chunk_size = 1024
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i:i + chunk_size]
                yield sample_rate, chunk
        else:
            log.error(f"Error: google return a response without audio")
            yield None
    except Exception as e:
        log.error(f"Error during google tts: {e}")
        yield None
