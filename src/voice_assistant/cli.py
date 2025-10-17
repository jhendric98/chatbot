"""Command-line interface for the voice assistant."""
from __future__ import annotations

import argparse
import logging
import sys
from typing import Optional

from voice_assistant.assistant import VoiceAssistant
from voice_assistant.config import AssistantConfig


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for the voice assistant demo."""
    parser = argparse.ArgumentParser(
        description="Voice assistant that listens for a keyword, records a prompt, and answers with OpenAI."
    )
    parser.add_argument("--keyword", default="genius", help="Wake word that activates recording (default: genius)")
    parser.add_argument(
        "--api-key", dest="api_key", help="OpenAI API key. Falls back to OPENAI_API_KEY environment variable"
    )
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
    """Configure logging with the specified level."""
    logging.basicConfig(level=getattr(logging, level), format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the voice assistant CLI."""
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

