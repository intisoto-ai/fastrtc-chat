import os
import pytest
from unittest import mock
import numpy as np
from fastrtc_chat.google_tts import create_google_tts_client, google_text_to_speech

@pytest.fixture
def mock_google_tts_client():
    with mock.patch('fastrtc_chat.google_tts.texttospeech.TextToSpeechClient') as mock_client:
        yield mock_client

def test_create_google_tts_client_with_credentials(mock_google_tts_client):
    mock_google_tts_client.return_value = mock.Mock()
    client = create_google_tts_client('fake_credentials.json')
    assert client is not None
    mock_google_tts_client.assert_called_once()

def test_create_google_tts_client_without_credentials(mock_google_tts_client):
    mock_google_tts_client.return_value = mock.Mock()
    client = create_google_tts_client()
    assert client is not None
    mock_google_tts_client.assert_called_once()

def test_google_text_to_speech(mock_google_tts_client):
    mock_google_tts_client.return_value.synthesize_speech.return_value.audio_content = b'\x00\x01'
    client = create_google_tts_client()
    text = "Hello, world!"
    result = list(google_text_to_speech(text))
    assert len(result) > 0
    assert result[0][0] == 16000  # sample rate
    assert isinstance(result[0][1], np.ndarray)

if __name__ == "__main__":
    pytest.main()