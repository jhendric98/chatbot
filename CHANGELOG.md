# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Professional repository documentation (CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT)
- GitHub issue and pull request templates
- Continuous integration workflow with GitHub Actions
- Comprehensive test suite with 79% coverage

## [0.1.0] - 2025-10-17

### Added

- Complete refactor to Python packaging best practices with `src/` layout
- Structured package with proper `__init__.py`, `__main__.py`, and modular design
- Comprehensive test suite with 44 tests across 4 test modules
- Test coverage reporting with pytest-cov (79% coverage)
- Professional project structure with `pyproject.toml`
- Type hints throughout the codebase
- Installable CLI command `voice-assistant`
- Support for programmatic usage as a Python package
- Export of main classes and functions for easy importing
- Development dependencies and tooling (pytest, ruff, pytest-cov)
- Locked dependencies with `uv.lock` for reproducibility

### Changed

- Migrated from single-file script to proper Python package
- Improved configuration with dedicated `AssistantConfig` dataclass
- Enhanced CLI with comprehensive argument parsing
- Updated README with extensive documentation
- Better error handling and logging throughout

### Fixed

- Audio processing reliability improvements
- Wake word detection accuracy
- Speech recognition error handling

## [0.0.2] - 2025-09-28

### Added

- UV project configuration for fast dependency management
- Professional README with comprehensive documentation
- Installation instructions for multiple platforms
- Command-line options documentation
- Troubleshooting section
- SECURITY.md file with security policy

### Changed

- Hardened voice assistant implementation
- Improved error handling and resilience
- Updated dependencies to latest stable versions

### Fixed

- Speech recognition output issues with Google Speech Recognition API
- Audio encoder compatibility problems

## [0.0.1] - 2023-04-18

### Added

- Initial voice assistant implementation
- Wake word detection using speech recognition
- OpenAI GPT integration for intelligent responses
- Text-to-speech output using gTTS
- Microphone input handling with PyAudio
- Basic command-line interface
- Requirements.txt for dependency management
- Initial README documentation

### Fixed

- Speech encoder compatibility (migrated to Google Speech Recognition)
- Audio playback issues

## [0.0.0] - 2023-04-05

### Added

- Initial project setup
- Basic project structure
- Initial README with project goals
- Git repository initialization

---

## Version History

- **0.1.0** (2025-10-17) - Major refactor to professional Python package
- **0.0.2** (2025-09-28) - UV integration and documentation improvements
- **0.0.1** (2023-04-18) - Initial working implementation
- **0.0.0** (2023-04-05) - Project inception

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this project.

## Links

- [Repository](https://github.com/yourusername/voice-assistant-demo)
- [Issues](https://github.com/yourusername/voice-assistant-demo/issues)
- [Pull Requests](https://github.com/yourusername/voice-assistant-demo/pulls)
