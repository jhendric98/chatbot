"""Tests for AssistantConfig dataclass."""

from voice_assistant import AssistantConfig


def test_config_default_values():
    """Test that AssistantConfig has correct default values."""
    config = AssistantConfig()

    assert config.keyword == "genius"
    assert config.model == "gpt-3.5-turbo"
    assert config.temperature == 0.7
    assert config.max_output_tokens == 400
    assert config.pause_threshold == 0.8
    assert config.ambient_noise_duration == 0.5
    assert config.listen_timeout is None
    assert config.phrase_time_limit is None


def test_config_custom_values():
    """Test that AssistantConfig accepts custom values."""
    config = AssistantConfig(
        keyword="hello",
        model="gpt-4o",
        temperature=1.0,
        max_output_tokens=500,
        pause_threshold=1.2,
        ambient_noise_duration=1.0,
        listen_timeout=10.0,
        phrase_time_limit=5.0,
    )

    assert config.keyword == "hello"
    assert config.model == "gpt-4o"
    assert config.temperature == 1.0
    assert config.max_output_tokens == 500
    assert config.pause_threshold == 1.2
    assert config.ambient_noise_duration == 1.0
    assert config.listen_timeout == 10.0
    assert config.phrase_time_limit == 5.0


def test_config_partial_override():
    """Test that AssistantConfig can partially override defaults."""
    config = AssistantConfig(keyword="computer", temperature=0.5)

    assert config.keyword == "computer"
    assert config.temperature == 0.5
    # Check that other defaults remain unchanged
    assert config.model == "gpt-3.5-turbo"
    assert config.max_output_tokens == 400
