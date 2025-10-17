"""Integration tests for the voice assistant."""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest
import speech_recognition as sr


class TestVoiceAssistantIntegration:
    """Integration tests for complete workflows."""

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_await_keyword_detected(
        self, mock_mic_class, voice_assistant, mock_audio_data
    ):
        """Test wake word detection workflow."""
        # Setup
        mock_mic = MagicMock()
        mock_mic.__enter__ = Mock(return_value=mock_mic)
        mock_mic.__exit__ = Mock(return_value=False)
        mock_mic_class.return_value = mock_mic

        voice_assistant.recognizer.listen = Mock(return_value=mock_audio_data)
        voice_assistant.recognizer.recognize_google = Mock(return_value="test")
        voice_assistant.recognizer.adjust_for_ambient_noise = Mock()

        # Execute
        result = voice_assistant._await_keyword()

        # Verify
        assert result is True
        voice_assistant.recognizer.adjust_for_ambient_noise.assert_called_once()
        voice_assistant.recognizer.listen.assert_called_once()

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_await_keyword_not_detected(
        self, mock_mic_class, voice_assistant, mock_audio_data
    ):
        """Test wake word not detected."""
        # Setup
        mock_mic = MagicMock()
        mock_mic.__enter__ = Mock(return_value=mock_mic)
        mock_mic.__exit__ = Mock(return_value=False)
        mock_mic_class.return_value = mock_mic

        voice_assistant.recognizer.listen = Mock(return_value=mock_audio_data)
        voice_assistant.recognizer.recognize_google = Mock(return_value="wrong word")
        voice_assistant.recognizer.adjust_for_ambient_noise = Mock()

        # Execute
        result = voice_assistant._await_keyword()

        # Verify
        assert result is False

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_await_keyword_timeout(self, mock_mic_class, voice_assistant):
        """Test wake word detection timeout."""
        # Setup
        mock_mic = MagicMock()
        mock_mic.__enter__ = Mock(return_value=mock_mic)
        mock_mic.__exit__ = Mock(return_value=False)
        mock_mic_class.return_value = mock_mic

        voice_assistant.recognizer.listen = Mock(side_effect=sr.WaitTimeoutError())
        voice_assistant.recognizer.adjust_for_ambient_noise = Mock()

        # Execute
        result = voice_assistant._await_keyword()

        # Verify
        assert result is False

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_capture_question_success(
        self, mock_mic_class, voice_assistant, mock_audio_data
    ):
        """Test successful question capture."""
        # Setup
        mock_mic = MagicMock()
        mock_mic.__enter__ = Mock(return_value=mock_mic)
        mock_mic.__exit__ = Mock(return_value=False)
        mock_mic_class.return_value = mock_mic

        voice_assistant.recognizer.listen = Mock(return_value=mock_audio_data)
        voice_assistant.recognizer.recognize_google = Mock(
            return_value="What is the weather?"
        )
        voice_assistant.recognizer.adjust_for_ambient_noise = Mock()

        # Execute
        result = voice_assistant._capture_question()

        # Verify
        assert result == "What is the weather?"

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_capture_question_timeout(self, mock_mic_class, voice_assistant):
        """Test question capture timeout."""
        # Setup
        mock_mic = MagicMock()
        mock_mic.__enter__ = Mock(return_value=mock_mic)
        mock_mic.__exit__ = Mock(return_value=False)
        mock_mic_class.return_value = mock_mic

        voice_assistant.recognizer.listen = Mock(side_effect=sr.WaitTimeoutError())
        voice_assistant.recognizer.adjust_for_ambient_noise = Mock()

        # Execute and verify
        with pytest.raises(RuntimeError, match="Timed out"):
            voice_assistant._capture_question()

    @patch("voice_assistant.assistant.sr.Microphone")
    def test_capture_question_microphone_error(self, mock_mic_class, voice_assistant):
        """Test question capture with microphone error."""
        # Setup - microphone not available
        mock_mic_class.side_effect = OSError("Microphone not found")

        # Execute and verify
        with pytest.raises(RuntimeError, match="Microphone is not available"):
            voice_assistant._capture_question()

    def test_full_response_generation_flow(self, voice_assistant, mock_openai_client):
        """Test complete flow from prompt to response."""
        voice_assistant.client = mock_openai_client

        # Simulate user asking a question
        question = "What is Python?"
        response = voice_assistant.generate_response(question)

        # Verify response was generated
        assert response == "This is a test response"

        # Verify OpenAI was called with correct structure
        call_kwargs = mock_openai_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == voice_assistant.config.model
        assert call_kwargs["temperature"] == voice_assistant.config.temperature
        assert len(call_kwargs["messages"]) == 2
        assert call_kwargs["messages"][1]["content"] == question
