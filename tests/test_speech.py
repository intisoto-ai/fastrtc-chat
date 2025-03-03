import pytest
from unittest import mock
import numpy as np
from fastrtc_chat.speech import speech_to_text, text_to_speech, process_audio
from fastrtc import get_stt_model


# Mock the STTModel and its stt method
class MockSTTModel:
    def stt(self, audio):
        return "Mocked transcribed text"

@pytest.fixture(autouse=True)
def mock_stt_model(monkeypatch):
    """Mocks the STTModel and its stt method."""
    monkeypatch.setattr("fastrtc_chat.speech.stt_model", MockSTTModel())


# Mock the google_text_to_speech function
@pytest.fixture
def mock_google_text_to_speech(monkeypatch):
    def mock_generator(text):
        yield 16000, np.array([1, 2, 3])  # Mock sample_rate and audio chunk
        yield 16000, np.array([4,5,6])
        yield None
    monkeypatch.setattr("fastrtc_chat.speech.google_text_to_speech", mock_generator)
    

@pytest.fixture
def mock_translate_text(monkeypatch):
    def mock_translation(text, target_lang='es-US'):
        return "Texto traducido"
    monkeypatch.setattr("fastrtc_chat.speech.translate_text", mock_translation)


def test_speech_to_text(mock_stt_model):
    """Tests the speech_to_text function."""
    sample_rate = 16000
    audio = np.array([0.1, 0.2, 0.3])
    result = speech_to_text(sample_rate, audio)
    assert result == "Mocked transcribed text"


def test_text_to_speech(mock_google_text_to_speech):
    """Tests the text_to_speech function."""
    result = list(text_to_speech("Test text"))
    assert len(result) == 3
    assert result[0][0] == 16000
    assert isinstance(result[0][1], np.ndarray)

def test_process_audio(mock_stt_model, mock_google_text_to_speech, mock_translate_text):
    """Tests the process_audio function."""
    sample_rate = 16000
    audio_data = np.array([0.1, 0.2, 0.3])
    audio = (sample_rate, audio_data)
    result = list(process_audio(audio))
    assert len(result) == 3
    assert result[0][0] == 16000
    assert isinstance(result[0][1], np.ndarray)

def test_process_audio_error(mock_stt_model, mock_google_text_to_speech, mock_translate_text, monkeypatch):
    """Tests the process_audio function when there is an error."""
    def mock_stt_model_error(audio):
        raise Exception("Mocked error")
    monkeypatch.setattr("fastrtc_chat.speech.stt_model.stt", mock_stt_model_error)
    sample_rate = 16000
    audio_data = np.array([0.1, 0.2, 0.3])
    audio = (sample_rate, audio_data)
    result = list(process_audio(audio))
    assert len(result) == 1 and result[0] is None # Modified assert
