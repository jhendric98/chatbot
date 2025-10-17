"""Pytest configuration and shared fixtures."""

from __future__ import annotations

from unittest.mock import MagicMock, Mock

import pytest
import speech_recognition as sr

from voice_assistant import AssistantConfig, VoiceAssistant


@pytest.fixture
def mock_recognizer():
    """Create a mock speech recognizer."""
    recognizer = MagicMock(spec=sr.Recognizer)
    recognizer.pause_threshold = 0.8
    return recognizer


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    client = MagicMock()

    # Mock the completion response structure
    mock_message = Mock()
    mock_message.content = "This is a test response"

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_completion = Mock()
    mock_completion.choices = [mock_choice]

    client.chat.completions.create.return_value = mock_completion

    return client


@pytest.fixture
def assistant_config():
    """Create a default assistant configuration."""
    return AssistantConfig(
        keyword="test",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_output_tokens=400,
    )


@pytest.fixture
def voice_assistant(mock_recognizer, assistant_config, monkeypatch):
    """Create a VoiceAssistant instance with mocked dependencies."""
    # Mock the OpenAI API key
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

    assistant = VoiceAssistant(
        api_key="sk-test-key-12345",
        config=assistant_config,
        recognizer=mock_recognizer,
    )

    return assistant


@pytest.fixture
def mock_audio_data():
    """Create mock audio data."""
    return MagicMock(spec=sr.AudioData)


@pytest.fixture
def mock_microphone():
    """Create a mock microphone context manager."""
    mic = MagicMock(spec=sr.Microphone)
    mic.__enter__ = Mock(return_value=mic)
    mic.__exit__ = Mock(return_value=False)
    return mic
