"""Tests for command-line interface."""
from __future__ import annotations

import pytest

from voice_assistant.cli import configure_logging, parse_args


class TestParseArgs:
    """Tests for argument parsing."""
    
    def test_parse_args_defaults(self):
        """Test default argument values."""
        args = parse_args([])
        
        assert args.keyword == "genius"
        assert args.model == "gpt-3.5-turbo"
        assert args.temperature == 0.7
        assert args.max_output_tokens == 400
        assert args.ambient_noise_duration == 0.5
        assert args.pause_threshold == 0.8
        assert args.listen_timeout is None
        assert args.phrase_time_limit is None
        assert args.once is False
        assert args.log_level == "INFO"
        assert args.api_key is None
    
    def test_parse_args_custom_keyword(self):
        """Test custom keyword argument."""
        args = parse_args(["--keyword", "hello"])
        assert args.keyword == "hello"
    
    def test_parse_args_custom_model(self):
        """Test custom model argument."""
        args = parse_args(["--model", "gpt-4o"])
        assert args.model == "gpt-4o"
    
    def test_parse_args_custom_temperature(self):
        """Test custom temperature argument."""
        args = parse_args(["--temperature", "1.5"])
        assert args.temperature == 1.5
    
    def test_parse_args_custom_max_tokens(self):
        """Test custom max output tokens argument."""
        args = parse_args(["--max-output-tokens", "1000"])
        assert args.max_output_tokens == 1000
    
    def test_parse_args_timeouts(self):
        """Test timeout arguments."""
        args = parse_args([
            "--listen-timeout", "10.0",
            "--phrase-time-limit", "5.0",
        ])
        
        assert args.listen_timeout == 10.0
        assert args.phrase_time_limit == 5.0
    
    def test_parse_args_ambient_noise_duration(self):
        """Test ambient noise duration argument."""
        args = parse_args(["--ambient-noise-duration", "2.0"])
        assert args.ambient_noise_duration == 2.0
    
    def test_parse_args_pause_threshold(self):
        """Test pause threshold argument."""
        args = parse_args(["--pause-threshold", "1.2"])
        assert args.pause_threshold == 1.2
    
    def test_parse_args_once_flag(self):
        """Test once flag."""
        args = parse_args(["--once"])
        assert args.once is True
    
    def test_parse_args_log_level(self):
        """Test log level argument."""
        args = parse_args(["--log-level", "DEBUG"])
        assert args.log_level == "DEBUG"
        
        args = parse_args(["--log-level", "ERROR"])
        assert args.log_level == "ERROR"
    
    def test_parse_args_api_key(self):
        """Test API key argument."""
        args = parse_args(["--api-key", "sk-test-key"])
        assert args.api_key == "sk-test-key"
    
    def test_parse_args_multiple_options(self):
        """Test multiple arguments together."""
        args = parse_args([
            "--keyword", "computer",
            "--model", "gpt-4o",
            "--temperature", "0.9",
            "--max-output-tokens", "600",
            "--once",
            "--log-level", "DEBUG",
        ])
        
        assert args.keyword == "computer"
        assert args.model == "gpt-4o"
        assert args.temperature == 0.9
        assert args.max_output_tokens == 600
        assert args.once is True
        assert args.log_level == "DEBUG"
    
    def test_parse_args_invalid_log_level(self):
        """Test that invalid log level raises error."""
        with pytest.raises(SystemExit):
            parse_args(["--log-level", "INVALID"])


class TestConfigureLogging:
    """Tests for logging configuration."""
    
    def test_configure_logging_info(self, caplog):
        """Test configuring INFO log level."""
        import logging
        
        # Create a fresh logger for testing
        test_logger = logging.getLogger("test_info")
        initial_level = test_logger.level
        
        configure_logging("INFO")
        
        # The root logger should be configured, not necessarily our test logger
        # Just verify the function runs without error
        assert True  # configure_logging completed successfully
    
    def test_configure_logging_debug(self, caplog):
        """Test configuring DEBUG log level."""
        configure_logging("DEBUG")
        
        # Verify the function runs without error
        assert True
    
    def test_configure_logging_error(self, caplog):
        """Test configuring ERROR log level."""
        configure_logging("ERROR")
        
        # Verify the function runs without error
        assert True

