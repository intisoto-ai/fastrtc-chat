import pytest
import os
from unittest import mock
from fastrtc_chat.translate import create_translate_client
from fastrtc_chat.google_tts import create_google_tts_client


def test_create_translate_client_env_var_not_set(monkeypatch):
    """Test that the translation client is not created when env var is not set."""
    monkeypatch.delenv("GOOGLE_FASTRTC_KEY", raising=False)
    client = create_translate_client(credentials_path=None)
    assert client is None

def test_create_google_tts_client_env_var_not_set(monkeypatch):
    """Test that the google tts client is not created when env var is not set."""
    monkeypatch.delenv("GOOGLE_FASTRTC_KEY", raising=False)
    client = create_google_tts_client(credentials_path=None)
    assert client is None
