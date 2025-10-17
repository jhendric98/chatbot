"""Core voice assistant implementation."""

from __future__ import annotations

import contextlib
import logging
import os
import tempfile
from pathlib import Path

import pygame
import speech_recognition as sr
from gtts import gTTS
from gtts.tts import gTTSError
from openai import OpenAI

from voice_assistant.config import AssistantConfig

LOGGER = logging.getLogger(__name__)


class VoiceAssistant:
    """Speech-driven assistant that delegates answers to the OpenAI API."""

    def __init__(
        self,
        api_key: str | None = None,
        config: AssistantConfig | None = None,
        recognizer: sr.Recognizer | None = None,
    ) -> None:
        self.config = config or AssistantConfig()
        self.recognizer = recognizer or sr.Recognizer()
        self.recognizer.pause_threshold = self.config.pause_threshold
        self.client = OpenAI(api_key=self._resolve_api_key(api_key))

    @staticmethod
    def _resolve_api_key(explicit: str | None) -> str:
        key = explicit or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "An OpenAI API key is required. Supply it with --api-key or the OPENAI_API_KEY environment variable."
            )
        return key

    def run(self, *, once: bool = False) -> None:
        """Start the main interaction loop."""
        LOGGER.info(
            "Starting voice assistant; waiting for keyword '%s'", self.config.keyword
        )
        try:
            while True:
                if not self._await_keyword():
                    continue

                try:
                    question = self._capture_question()
                except RuntimeError as exc:  # microphone failure
                    LOGGER.error("Could not capture question: %s", exc)
                    continue

                if not question:
                    LOGGER.warning("No speech detected after keyword; waiting again")
                    if once:
                        break
                    continue

                LOGGER.info("User said: %s", question)

                try:
                    response = self.generate_response(question)
                except Exception:  # pragma: no cover - network/API errors
                    LOGGER.exception("Failed to fetch response from OpenAI")
                    if once:
                        break
                    continue

                LOGGER.info("Assistant response: %s", response)
                self.speak_text(response)

                if once:
                    break
        except KeyboardInterrupt:
            LOGGER.info("Received interrupt; shutting down")

    def _await_keyword(self) -> bool:
        """Listen until the configured keyword is spoken."""
        LOGGER.debug("Listening for wake word")
        print(f"Say '{self.config.keyword}' to start recording your question...")
        try:
            with sr.Microphone() as source:
                self._prepare_microphone(source)
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.config.listen_timeout,
                        phrase_time_limit=self.config.phrase_time_limit,
                    )
                except sr.WaitTimeoutError:
                    LOGGER.debug("Keyword listen timed out")
                    return False
        except OSError as exc:
            LOGGER.error("Microphone is not available: %s", exc)
            return False

        transcription = self._recognize_speech(audio)
        LOGGER.debug("Wake-word transcription: %s", transcription)
        return bool(
            transcription
            and transcription.lower().strip() == self.config.keyword.lower()
        )

    def _capture_question(self) -> str | None:
        """Record and transcribe the user's question."""
        print("Keyword detected. Ask your question after the tone!")
        try:
            with sr.Microphone() as source:
                self._prepare_microphone(source)
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.config.listen_timeout,
                        phrase_time_limit=self.config.phrase_time_limit,
                    )
                except sr.WaitTimeoutError as exc:
                    raise RuntimeError("Timed out waiting for a question") from exc
        except OSError as exc:
            raise RuntimeError("Microphone is not available") from exc

        return self._recognize_speech(audio)

    def _prepare_microphone(self, source: sr.AudioSource) -> None:
        """Calibrate for background noise before recording."""
        self.recognizer.adjust_for_ambient_noise(
            source, duration=self.config.ambient_noise_duration
        )

    def _recognize_speech(self, audio: sr.AudioData) -> str | None:
        """Transcribe recorded audio with Google's speech recognition service."""
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            LOGGER.warning("Speech was unintelligible")
        except sr.RequestError as exc:
            LOGGER.error("Speech recognition service unavailable: %s", exc)
        return None

    def generate_response(self, prompt: str) -> str:
        """Generate a reply for the supplied prompt using the OpenAI Chat Completions API."""
        if not prompt.strip():
            raise ValueError("Prompt must contain text")

        completion = self.client.chat.completions.create(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_output_tokens,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful voice assistant that gives concise answers.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        try:
            message = completion.choices[0].message
        except (IndexError, AttributeError) as exc:
            raise RuntimeError("OpenAI response did not contain any choices") from exc

        if not message or not getattr(message, "content", None):
            raise RuntimeError("OpenAI returned an empty response")

        return message.content

    def speak_text(self, text: str) -> None:
        """Convert text to speech using gTTS and play the generated audio."""
        if not text.strip():
            LOGGER.debug("Skipping empty response")
            return

        with tempfile.NamedTemporaryFile(
            prefix="assistant_", suffix=".mp3", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            gTTS(text=text, lang="en", slow=False).save(str(temp_path))
        except gTTSError as exc:
            LOGGER.error("Failed to synthesize speech with gTTS: %s", exc)
            return

        try:
            # Initialize pygame mixer if not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Load and play the audio file
            pygame.mixer.music.load(str(temp_path))
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as exc:
            LOGGER.error("Unable to play synthesized speech: %s", exc)
        finally:
            # Stop and unload the music
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            # Clean up the temporary file
            with contextlib.suppress(OSError):
                temp_path.unlink()
