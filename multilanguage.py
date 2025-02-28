import os
import logging
from fastrtc import Stream, ReplyOnPause, get_stt_model, get_tts_model
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def create_translate_client(credentials_path=None):
    """Creates a Google Translate client, optionally using a service account file."""
    if credentials_path:
        try:
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            return translate.Client(credentials=credentials)
        except Exception as e:
            logger.error(f"Error loading credentials from {credentials_path}: {e}")
            return None
    else:
        return translate.Client()
# Initialize models
try:
    stt_model = get_stt_model()
except Exception as e:
    logger.error(f"Error initializing STT model: {e}")
    exit()

try:
    tts_model = get_tts_model()
except Exception as e:
    logger.error(f"Error initializing TTS model: {e}")
    exit()

translate_client = create_translate_client("./path/to/your/credentials.json")  # Optional: Replace with your credentials file
if translate_client is None:
    logger.error("Failed to initialize translation client. Check your credentials.")
    exit()


def translate_text(text, target_lang='es'):
    """
    Translates text to the target language using Google Cloud Translation API.
    """
    try:
        output = translate_client.translate(text, target_language=target_lang)
        return output['translatedText']
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return "Error during translation"


def chat_handler(audio: tuple[int, np.ndarray], target_lang='es'):
    """
    Processes incoming audio, translates it, and returns audio in the target language.
    """
    try:
        # Step 1: Convert audio input to text
        input_text = stt_model.stt(audio)
        logger.info(f"Input Text: {input_text}")

        # Step 2: Translate the recognized text
        translated_text = translate_text(input_text, target_lang=target_lang)
        logger.info(f"Translated Text: {translated_text}")

        # Step 3: Convert the translated text back to audio
        for audio_chunk in tts_model.stream_tts_sync(translated_text):
            yield audio_chunk
    except Exception as e:
        logger.error(f"Error during chat processing: {e}")
        # You might yield an error audio chunk or take other actions here

# Create and launch the stream
stream = Stream(ReplyOnPause(lambda audio: chat_handler(audio, target_lang='fr')), modality="audio", mode="send-receive")
stream.ui.launch()
