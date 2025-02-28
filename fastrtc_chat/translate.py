from google.cloud import translate_v2 as translate

# Initialize Google Translate API
translate_client = translate.Client()

def translate_text(text, target_lang='es'):
    """Translates text to the target language."""
    result = translate_client.translate(text, target_language=target_lang)
    return result['translatedText']
