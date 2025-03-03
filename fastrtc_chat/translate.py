# fastrtc_chat/translate.py
import os
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import logging

log = logging.getLogger(__name__)
# Configure logging
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def create_translate_client(credentials_path=None):
    """Creates a Google Translate client, optionally using a service account file."""
    if credentials_path:
        try:
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            return translate.Client(credentials=credentials)
        except Exception as e:
            log.error(f"Error loading credentials from {credentials_path}: {e}")
            return None
    else:
        if os.environ.get("GOOGLE_FASTRTC_KEY") is None:
            log.error("Environment variable GOOGLE_FASTRTC_KEY is not set")
            return None
        return translate.Client()


def translate_text(text, target_language='es-US', client=None):
    """Translates text to the target language."""
    if client is None:
        credentials_path = os.environ.get("GOOGLE_FASTRTC_KEY") # Now using the env variable
        if credentials_path is None:
            log.error("Error: Environment variable GOOGLE_FASTRTC_KEY is not set")
            return "Error during translation"
        client = create_translate_client(credentials_path)

        if client is None:
            log.error("Failed to initialize translation client. Check your credentials.")
            return "Error during translation"
    try:
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        log.error(f"Error during translation: {e}")
        return "Error during translation"

