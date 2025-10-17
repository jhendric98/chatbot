"""Voice assistant package that listens for a keyword, records a prompt, and answers with OpenAI."""

from voice_assistant.assistant import VoiceAssistant
from voice_assistant.config import AssistantConfig

__version__ = "0.1.0"

__all__ = [
    "VoiceAssistant",
    "AssistantConfig",
    "__version__",
]

