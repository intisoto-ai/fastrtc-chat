import pytest
from unittest import mock
from google.cloud import translate_v2 as translate
from fastrtc_chat.translate import translate_text, create_translate_client
import json
import os
from google.oauth2 import service_account


@pytest.fixture
def mock_translate_client(monkeypatch):
    """Mocks the translate.Client."""
    with mock.patch('fastrtc_chat.translate.translate.Client') as mock_client:
        yield mock_client


def test_create_translate_client_with_credentials(mock_translate_client, monkeypatch):
    """Test create_translate_client with credentials."""
    mock_translate_client.return_value = mock.Mock()
    #mock the from_service_account_file
    with mock.patch('fastrtc_chat.translate.service_account.Credentials.from_service_account_file') as mock_from_file:
        mock_from_file.return_value = mock.Mock()
        client = create_translate_client("fake_credentials.json")
        assert client is not None
        mock_translate_client.assert_called_once()
        mock_from_file.assert_called_once_with("fake_credentials.json")

def test_create_translate_client_without_credentials(mock_translate_client):
    """Test create_translate_client without credentials."""
    mock_translate_client.return_value = mock.Mock()
    client = create_translate_client()
    assert client is not None
    mock_translate_client.assert_called_once()

def test_translate_text(mock_translate_client):
    """Test translate_text function."""
    mock_instance = mock.Mock()
    mock_translate_client.return_value = mock_instance
    mock_instance.translate.return_value = {'translatedText': '¡Hola Mundo!'}

    text = "Hello, world!"
    client = create_translate_client()
    result = translate_text(text, client=mock_instance)
    assert result == "¡Hola Mundo!"
    mock_instance.translate.assert_called_with(text, target_language='es-US')

def test_translate_text_error(mock_translate_client):
    """Test translate_text function when an error occurs."""
    mock_instance = mock.Mock()
    mock_translate_client.return_value = mock_instance
    mock_instance.translate.side_effect = Exception("Mocked error")

    result = translate_text("some text", client=mock_instance)
    assert result == "Error during translation"
