"""Tests for VoiceAssistant class."""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest
import speech_recognition as sr

from voice_assistant import AssistantConfig, VoiceAssistant


class TestVoiceAssistantInit:
    """Tests for VoiceAssistant initialization."""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        assistant = VoiceAssistant(api_key="sk-test-key")

        assert assistant.client is not None
        assert assistant.config is not None
        assert assistant.recognizer is not None

    def test_init_with_env_api_key(self, monkeypatch):
        """Test initialization with environment variable API key."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-env-key")

        assistant = VoiceAssistant()

        assert assistant.client is not None

    def test_init_without_api_key_raises_error(self, monkeypatch):
        """Test that initialization without API key raises RuntimeError."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(RuntimeError, match="An OpenAI API key is required"):
            VoiceAssistant(api_key=None)

    def test_init_with_custom_config(self):
        """Test initialization with custom configuration."""
        config = AssistantConfig(keyword="test", model="gpt-4o")
        assistant = VoiceAssistant(api_key="sk-test", config=config)

        assert assistant.config.keyword == "test"
        assert assistant.config.model == "gpt-4o"

    def test_init_sets_pause_threshold(self):
        """Test that initialization sets recognizer pause threshold."""
        config = AssistantConfig(pause_threshold=1.5)
        recognizer = sr.Recognizer()

        assistant = VoiceAssistant(
            api_key="sk-test",
            config=config,
            recognizer=recognizer,
        )

        assert assistant.recognizer.pause_threshold == 1.5


class TestGenerateResponse:
    """Tests for generate_response method."""

    def test_generate_response_success(self, voice_assistant, mock_openai_client):
        """Test successful response generation."""
        voice_assistant.client = mock_openai_client

        response = voice_assistant.generate_response("What is the weather?")

        assert response == "This is a test response"
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_generate_response_with_correct_parameters(
        self, voice_assistant, mock_openai_client
    ):
        """Test that generate_response calls OpenAI with correct parameters."""
        voice_assistant.client = mock_openai_client
        voice_assistant.config.model = "gpt-4o"
        voice_assistant.config.temperature = 0.9
        voice_assistant.config.max_output_tokens = 500

        voice_assistant.generate_response("Test prompt")

        call_kwargs = mock_openai_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o"
        assert call_kwargs["temperature"] == 0.9
        assert call_kwargs["max_tokens"] == 500
        assert len(call_kwargs["messages"]) == 2
        assert call_kwargs["messages"][0]["role"] == "system"
        assert call_kwargs["messages"][1]["role"] == "user"
        assert call_kwargs["messages"][1]["content"] == "Test prompt"

    def test_generate_response_empty_prompt_raises_error(self, voice_assistant):
        """Test that empty prompt raises ValueError."""
        with pytest.raises(ValueError, match="Prompt must contain text"):
            voice_assistant.generate_response("")

        with pytest.raises(ValueError, match="Prompt must contain text"):
            voice_assistant.generate_response("   ")

    def test_generate_response_no_choices_raises_error(
        self, voice_assistant, mock_openai_client
    ):
        """Test that response without choices raises RuntimeError."""
        voice_assistant.client = mock_openai_client
        mock_openai_client.chat.completions.create.return_value.choices = []

        with pytest.raises(RuntimeError, match="did not contain any choices"):
            voice_assistant.generate_response("Test")

    def test_generate_response_empty_content_raises_error(
        self, voice_assistant, mock_openai_client
    ):
        """Test that response with empty content raises RuntimeError."""
        voice_assistant.client = mock_openai_client

        mock_message = Mock()
        mock_message.content = None
        mock_openai_client.chat.completions.create.return_value.choices[0].message = (
            mock_message
        )

        with pytest.raises(RuntimeError, match="returned an empty response"):
            voice_assistant.generate_response("Test")


class TestRecognizeSpeech:
    """Tests for _recognize_speech method."""

    def test_recognize_speech_success(self, voice_assistant, mock_audio_data):
        """Test successful speech recognition."""
        voice_assistant.recognizer.recognize_google = Mock(return_value="hello world")

        result = voice_assistant._recognize_speech(mock_audio_data)

        assert result == "hello world"
        voice_assistant.recognizer.recognize_google.assert_called_once_with(
            mock_audio_data
        )

    def test_recognize_speech_unknown_value(self, voice_assistant, mock_audio_data):
        """Test speech recognition with unintelligible audio."""
        voice_assistant.recognizer.recognize_google = Mock(
            side_effect=sr.UnknownValueError()
        )

        result = voice_assistant._recognize_speech(mock_audio_data)

        assert result is None

    def test_recognize_speech_request_error(self, voice_assistant, mock_audio_data):
        """Test speech recognition with service error."""
        voice_assistant.recognizer.recognize_google = Mock(
            side_effect=sr.RequestError("Service unavailable")
        )

        result = voice_assistant._recognize_speech(mock_audio_data)

        assert result is None


class TestSpeakText:
    """Tests for speak_text method."""

    def test_speak_text_empty_string_skips(self, voice_assistant):
        """Test that empty text is skipped."""
        with patch("voice_assistant.assistant.gTTS") as mock_gtts:
            voice_assistant.speak_text("")
            mock_gtts.assert_not_called()

            voice_assistant.speak_text("   ")
            mock_gtts.assert_not_called()

    @patch("voice_assistant.assistant.pygame")
    @patch("voice_assistant.assistant.gTTS")
    @patch("voice_assistant.assistant.tempfile.NamedTemporaryFile")
    def test_speak_text_success(
        self, mock_temp, mock_gtts, mock_pygame, voice_assistant
    ):
        """Test successful text-to-speech."""
        # Setup mocks
        mock_file = MagicMock()
        mock_file.name = "/tmp/test.mp3"
        mock_temp.return_value.__enter__.return_value = mock_file

        mock_gtts_instance = MagicMock()
        mock_gtts.return_value = mock_gtts_instance

        mock_pygame.mixer.get_init.return_value = True
        mock_pygame.mixer.music.get_busy.side_effect = [True, True, False]

        # Execute
        voice_assistant.speak_text("Hello world")

        # Verify
        mock_gtts.assert_called_once_with(text="Hello world", lang="en", slow=False)
        mock_gtts_instance.save.assert_called_once()
        mock_pygame.mixer.music.load.assert_called_once()
        mock_pygame.mixer.music.play.assert_called_once()

    @patch("voice_assistant.assistant.gTTS")
    @patch("voice_assistant.assistant.tempfile.NamedTemporaryFile")
    def test_speak_text_gtts_error(self, mock_temp, mock_gtts, voice_assistant):
        """Test handling of gTTS errors."""
        from gtts.tts import gTTSError

        mock_file = MagicMock()
        mock_file.name = "/tmp/test.mp3"
        mock_temp.return_value.__enter__.return_value = mock_file

        mock_gtts.side_effect = gTTSError("Network error")

        # Should not raise, just log error
        voice_assistant.speak_text("Hello")

        mock_gtts.assert_called_once()

    @patch("voice_assistant.assistant.pygame")
    @patch("voice_assistant.assistant.gTTS")
    @patch("voice_assistant.assistant.tempfile.NamedTemporaryFile")
    def test_speak_text_pygame_error(
        self, mock_temp, mock_gtts, mock_pygame, voice_assistant
    ):
        """Test handling of pygame errors."""
        mock_file = MagicMock()
        mock_file.name = "/tmp/test.mp3"
        mock_temp.return_value.__enter__.return_value = mock_file

        mock_gtts_instance = MagicMock()
        mock_gtts.return_value = mock_gtts_instance

        mock_pygame.mixer.get_init.return_value = False
        mock_pygame.mixer.init.side_effect = Exception("Audio error")

        # Should not raise, just log error
        voice_assistant.speak_text("Hello")


class TestPrepareMincrophone:
    """Tests for _prepare_microphone method."""

    def test_prepare_microphone(self, voice_assistant):
        """Test microphone preparation."""
        mock_source = MagicMock()
        voice_assistant.config.ambient_noise_duration = 1.5

        voice_assistant._prepare_microphone(mock_source)

        voice_assistant.recognizer.adjust_for_ambient_noise.assert_called_once_with(
            mock_source, duration=1.5
        )
