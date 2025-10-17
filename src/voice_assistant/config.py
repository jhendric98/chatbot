"""Configuration for the voice assistant."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AssistantConfig:
    """Configuration options for :class:`VoiceAssistant`."""

    keyword: str = "genius"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_output_tokens: int = 400
    pause_threshold: float = 0.8
    ambient_noise_duration: float = 0.5
    listen_timeout: float | None = None
    phrase_time_limit: float | None = None
