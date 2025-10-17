# Contributing to Voice Assistant Demo

First off, thank you for considering contributing to Voice Assistant Demo! It's people like you that make this project such a great learning tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [What Should I Know Before I Get Started?](#what-should-i-know-before-i-get-started)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
  - [Documentation Styleguide](#documentation-styleguide)
- [Testing Guidelines](#testing-guidelines)
- [Additional Notes](#additional-notes)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## What Should I Know Before I Get Started?

### Project Goals

This project is intentionally designed as **training material** for learning modern Python development practices. When contributing, keep these goals in mind:

- **Educational**: Code should be clear, well-commented, and instructive
- **Simple**: Avoid over-engineering; prefer clarity over cleverness
- **Modern**: Use current Python best practices and tooling
- **Well-documented**: Every feature should be documented

### Project Structure

```text
voice-assistant-demo/
├── src/voice_assistant/      # Main package code
├── tests/                    # Test suite
├── .github/                  # GitHub templates and workflows
├── pyproject.toml           # Project configuration
├── uv.lock                  # Locked dependencies
└── README.md                # Main documentation
```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

**Good bug reports** include:

- **Clear title and description**
- **Exact steps to reproduce the problem**
- **Expected vs. actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Relevant logs or error messages**
- **Screenshots or recordings** (if applicable)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:

- **Clear use case**: Explain why this enhancement would be useful
- **Detailed description**: Describe the desired behavior
- **Alternatives considered**: What other approaches did you think about?
- **Additional context**: Screenshots, examples, or references

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Simple issues perfect for newcomers
- `help wanted` - Issues where we'd especially appreciate help
- `documentation` - Improvements to documentation
- `testing` - Adding or improving tests

### Pull Requests

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow our styleguides** (see below)

3. **Add tests** for new features or bug fixes

4. **Ensure tests pass**:
   ```bash
   uv run pytest -v
   ```

5. **Run the linter**:
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

6. **Update documentation** as needed (README, docstrings, etc.)

7. **Write a clear commit message** following our commit message convention

8. **Submit your pull request** using our [PR template](.github/PULL_REQUEST_TEMPLATE.md)

## Development Setup

### Prerequisites

- Python 3.9 or newer
- PortAudio (for PyAudio)
  - macOS: `brew install portaudio`
  - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`
  - Windows: [Download binaries](http://www.portaudio.com/download.html)

### Setup Steps

1. **Install uv** (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/voice-assistant-demo.git
   cd voice-assistant-demo
   ```

3. **Install dependencies** (includes dev tools):
   ```bash
   uv sync
   ```

4. **Verify installation**:
   ```bash
   uv run pytest -v
   uv run voice-assistant --help
   ```

5. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   cat > .git/hooks/pre-commit << 'EOF'
   #!/bin/sh
   echo "Running linter..."
   uv run ruff check . || exit 1
   echo "Running tests..."
   uv run pytest || exit 1
   EOF
   chmod +x .git/hooks/pre-commit
   ```

## Styleguides

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - ✨ `:sparkles:` - New feature
  - 🐛 `:bug:` - Bug fix
  - 📝 `:memo:` - Documentation
  - 🎨 `:art:` - Code structure/format
  - ⚡ `:zap:` - Performance improvement
  - ✅ `:white_check_mark:` - Adding tests
  - 🔒 `:lock:` - Security fix
  - ♻️ `:recycle:` - Refactoring
  - 🔧 `:wrench:` - Configuration changes

**Examples:**

```
✨ Add support for custom wake word phrases

Allows users to specify multi-word wake phrases instead of single words.
Closes #42
```

```
🐛 Fix microphone initialization on Windows

The microphone wasn't being properly released, causing errors on subsequent runs.
Fixes #38
```

### Python Styleguide

We use **Ruff** for linting and formatting. Key points:

- **Line length**: 120 characters maximum
- **Type hints**: Use throughout the codebase
- **Docstrings**: Use Google-style docstrings for all public functions/classes
- **Imports**: Sorted automatically by Ruff (isort)
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

**Example function with docstring:**

```python
def transcribe_audio(audio: sr.AudioData, language: str = "en-US") -> str:
    """Transcribe audio data to text using Google Speech Recognition.

    Args:
        audio: The audio data to transcribe.
        language: The language code for transcription (default: "en-US").

    Returns:
        The transcribed text as a string.

    Raises:
        sr.UnknownValueError: If speech is unintelligible.
        sr.RequestError: If the API is unreachable.
    """
    recognizer = sr.Recognizer()
    return recognizer.recognize_google(audio, language=language)
```

**Running the linter:**

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

### Documentation Styleguide

- **README**: Keep it comprehensive but organized with a clear table of contents
- **Code comments**: Explain *why*, not *what* (code should be self-documenting)
- **Docstrings**: Required for all public functions, classes, and modules
- **CHANGELOG**: Update for every user-facing change following [Keep a Changelog](https://keepachangelog.com/)
- **Examples**: Include code examples for new features

## Testing Guidelines

### Test Coverage Goals

- **Minimum**: 75% code coverage
- **Target**: 85%+ code coverage
- **New features**: Must include tests
- **Bug fixes**: Should include regression tests

### Writing Tests

1. **Use descriptive test names**:
   ```python
   def test_generate_response_handles_api_timeout():
       """Test that API timeouts are handled gracefully."""
       # Test implementation
   ```

2. **Follow AAA pattern** (Arrange, Act, Assert):
   ```python
   def test_wake_word_detection():
       # Arrange
       assistant = VoiceAssistant(api_key="test-key")
       audio = create_mock_audio("genius activate")
       
       # Act
       result = assistant.detect_wake_word(audio)
       
       # Assert
       assert result is True
   ```

3. **Use fixtures** from `conftest.py` to avoid duplication

4. **Mock external dependencies** (OpenAI API, microphone, etc.)

5. **Test edge cases** and error conditions

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_assistant.py

# Run specific test
uv run pytest tests/test_assistant.py::test_generate_response_success

# Run with coverage report
uv run pytest --cov=voice_assistant --cov-report=term-missing

# Run with HTML coverage report
uv run pytest --cov=voice_assistant --cov-report=html
# Open htmlcov/index.html to view results
```

## Additional Notes

### Issue and Pull Request Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue or PR already exists
- `invalid` - This doesn't seem right
- `testing` - Related to test suite

### Recognition

Contributors will be recognized in the following ways:

- Listed in CHANGELOG.md for their contributions
- Mentioned in release notes
- GitHub's contributor graph
- Shoutouts in README acknowledgments (for significant contributions)

### Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/yourusername/voice-assistant-demo/discussions)
- **Stuck?** Comment on the issue you're working on
- **Need clarification?** Tag maintainers in your PR or issue

### Philosophy

Remember: **This is a learning project.** We value:

1. **Education over perfection** - Clear, instructive code beats clever optimizations
2. **Collaboration over competition** - Help each other learn and grow
3. **Progress over perfection** - Incremental improvements are welcomed
4. **Kindness always** - Be respectful, patient, and constructive

---

Thank you for contributing to Voice Assistant Demo! 🎉

Your contributions help make this a better learning resource for everyone.

