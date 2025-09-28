"""Voice assistant demo that listens for a keyword, records a prompt, and answers with OpenAI."""
from __future__ import annotations

import argparse
import contextlib
import logging
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import speech_recognition as sr
from gtts import gTTS
from gtts.tts import gTTSError
from openai import OpenAI
from playsound import PlaysoundException, playsound

LOGGER = logging.getLogger(__name__)


@dataclass
class AssistantConfig:
    """Configuration options for :class:`VoiceAssistant`."""

    keyword: str = "genius"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_output_tokens: int = 400
    pause_threshold: float = 0.8
    ambient_noise_duration: float = 0.5
    listen_timeout: Optional[float] = None
    phrase_time_limit: Optional[float] = None


class VoiceAssistant:
    """Speech-driven assistant that delegates answers to the OpenAI API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[AssistantConfig] = None,
        recognizer: Optional[sr.Recognizer] = None,
    ) -> None:
        self.config = config or AssistantConfig()
        self.recognizer = recognizer or sr.Recognizer()
        self.recognizer.pause_threshold = self.config.pause_threshold
        self.client = OpenAI(api_key=self._resolve_api_key(api_key))

    @staticmethod
    def _resolve_api_key(explicit: Optional[str]) -> str:
        key = explicit or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "An OpenAI API key is required. Supply it with --api-key or the OPENAI_API_KEY environment variable."
            )
        return key

    def run(self, *, once: bool = False) -> None:
        """Start the main interaction loop."""
        LOGGER.info("Starting voice assistant; waiting for keyword '%s'", self.config.keyword)
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
        return bool(transcription and transcription.lower().strip() == self.config.keyword.lower())

    def _capture_question(self) -> Optional[str]:
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
        self.recognizer.adjust_for_ambient_noise(source, duration=self.config.ambient_noise_duration)

    def _recognize_speech(self, audio: sr.AudioData) -> Optional[str]:
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

        with tempfile.NamedTemporaryFile(prefix="assistant_", suffix=".mp3", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            gTTS(text=text, lang="en", slow=False).save(str(temp_path))
        except gTTSError as exc:
            LOGGER.error("Failed to synthesize speech with gTTS: %s", exc)
            return

        try:
            playsound(str(temp_path))
        except PlaysoundException as exc:
            LOGGER.error("Unable to play synthesized speech: %s", exc)
        finally:
            with contextlib.suppress(OSError):
                temp_path.unlink()


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for the voice assistant demo."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keyword", default="genius", help="Wake word that activates recording (default: genius)")
    parser.add_argument("--api-key", dest="api_key", help="OpenAI API key. Falls back to OPENAI_API_KEY environment variable")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Chat model to request from OpenAI")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature for the model")
    parser.add_argument("--max-output-tokens", type=int, default=400, help="Maximum number of tokens in the response")
    parser.add_argument(
        "--listen-timeout", type=float, default=None, help="Seconds to wait for speech before timing out"
    )
    parser.add_argument(
        "--phrase-time-limit", type=float, default=None, help="Maximum number of seconds to record once speech starts"
    )
    parser.add_argument(
        "--ambient-noise-duration",
        type=float,
        default=0.5,
        help="Seconds to sample background noise before each recording",
    )
    parser.add_argument(
        "--pause-threshold",
        type=float,
        default=0.8,
        help="Seconds of silence that will mark the end of a phrase",
    )
    parser.add_argument("--once", action="store_true", help="Exit after answering a single question")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Logging verbosity",
    )
    return parser.parse_args(argv)


def configure_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level), format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    configure_logging(args.log_level)

    config = AssistantConfig(
        keyword=args.keyword,
        model=args.model,
        temperature=args.temperature,
        max_output_tokens=args.max_output_tokens,
        listen_timeout=args.listen_timeout,
        phrase_time_limit=args.phrase_time_limit,
        ambient_noise_duration=args.ambient_noise_duration,
        pause_threshold=args.pause_threshold,
    )

    assistant = VoiceAssistant(api_key=args.api_key, config=config)
    assistant.run(once=args.once)
    return 0


if __name__ == "__main__":
    sys.exit(main())
