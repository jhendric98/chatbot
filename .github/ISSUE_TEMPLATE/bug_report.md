---
name: Bug Report
about: Create a report to help us improve the Voice Assistant Demo
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Bug Description

### Describe the bug

A clear and concise description of what the bug is.

### Expected behavior

A clear and concise description of what you expected to happen.

### Actual behavior

A clear and concise description of what actually happened.

## Reproduction Steps

### To Reproduce

Steps to reproduce the behavior:

1. Run command '...'
2. Say wake word '...'
3. Speak question '...'
4. See error

### Minimal example

If possible, provide the minimal command or code that reproduces the issue:

```bash
uv run voice-assistant --keyword "test" --log-level DEBUG
```

## Environment Information

### System Information

- OS: [e.g., macOS 13.0, Ubuntu 22.04, Windows 11]
- Python version: [e.g., 3.11.5]
- Package manager: [e.g., uv 0.1.0, pip 23.0]

### Project Information

- Voice Assistant Demo version: [e.g., 0.1.0]
- Installation method: [e.g., `uv sync`, `pip install -e .`]

### Dependencies

Run `uv run python -c "import sys; print(sys.version)"` and paste the output:

```text
[Paste output here]
```

**Audio Setup:**

- Microphone: [e.g., Built-in, USB headset, etc.]
- Audio output: [e.g., Built-in speakers, headphones, etc.]
- PortAudio version: [if known]

## Error Details

### Error messages

If applicable, paste the full error message:

```text
[Paste error message here]
```

### Log output

Run with `--log-level DEBUG` and paste relevant log output:

```text
[Paste debug logs here]
```

### Stack trace

If there's a Python traceback, paste it here:

```text
[Paste stack trace here]
```

## Additional Context

### Screenshots

If applicable, add screenshots to help explain your problem.

### Configuration

If you're using custom configuration, please share relevant settings:

- Wake word: [e.g., "genius"]
- OpenAI model: [e.g., "gpt-3.5-turbo"]
- Custom command-line options: [e.g., --temperature 0.9]

### Workarounds

Have you found any temporary workarounds for this issue?

### Additional context

Add any other context about the problem here.

## Checklist

Before submitting, please check:

- [ ] I have searched existing issues to avoid duplicates
- [ ] I have included all required environment information
- [ ] I have provided clear reproduction steps
- [ ] I have included relevant error messages and logs
- [ ] I have tested with the latest version of the project
- [ ] I have verified that PortAudio is properly installed
- [ ] I have confirmed my OpenAI API key is valid (if relevant)

## Educational Context

**Learning goals**
If this is for educational purposes, what are you trying to learn or demonstrate?

**Workshop/Course context**
Are you using this in a workshop, course, or tutorial? Please provide context.

---

**Note**: This project is designed for educational purposes. If you're using it in a production environment, please note that additional hardening may be required.
