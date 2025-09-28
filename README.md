# Voice Assistant Training Demo

A microphone-driven assistant that listens for a configurable wake word, records a spoken question, and uses the OpenAI API to
produce and read an answer aloud. This repository is intentionally lightweight so it can be used as training material for
exploring speech recognition, text-to-speech, and large language model integrations in Python.

## Features

- Automatic noise calibration and wake-word detection before capturing a question
- Google Speech Recognition transcription of recorded audio
- Configurable OpenAI Chat Completions integration (model, temperature, token limits, etc.)
- Text-to-speech responses delivered through gTTS and played locally
- Command line options to tailor the experience for workshops and demonstrations

## Requirements

- Python 3.9 or newer
- A working microphone connected to the machine running the demo
- An OpenAI API key with access to the selected chat model
- PortAudio libraries (required by `pyaudio`)

### Installing PortAudio

- **macOS**: `brew install portaudio`
- **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev`
- **Windows**: Install the latest [PortAudio binaries](http://www.portaudio.com/download.html) and ensure they are on the
  system `PATH` before installing `pyaudio`.

## Environment setup with `uv`

[`uv`](https://github.com/astral-sh/uv) offers a fast, isolated environment for Python projects. To set up the demo:

1. Install `uv` if it is not already available:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   On Windows you can use PowerShell:
   ```powershell
   powershell -ExecutionPolicy Bypass -File <(iwr https://astral.sh/uv/install.ps1)
   ```
2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install the project dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

If you prefer `pip`, replace step 3 with `pip install -r requirements.txt`.

## Configuration

Set your OpenAI API key in the environment before running the assistant:

```bash
export OPENAI_API_KEY="sk-your-key"
```

Environment variables are preferable to storing credentials in source files for training scenarios.

## Running the assistant

After activating the virtual environment and configuring the API key, launch the assistant:

```bash
python chatbot.py
```

By default the assistant listens for the wake word `"genius"`. Speak the keyword, wait for the prompt, and ask your question.
The answer will be displayed in the terminal and read aloud.

### Useful command line options

- `--keyword`: Change the wake word that begins recording.
- `--model`: Request a different OpenAI chat model (for example, `gpt-4o-mini`).
- `--temperature`: Adjusts the randomness of the generated response.
- `--max-output-tokens`: Limit the size of the response.
- `--listen-timeout` / `--phrase-time-limit`: Control how long the assistant waits for speech.
- `--once`: Exit after handling a single question (useful for demos).
- `--log-level`: Increase logging detail (e.g., `--log-level DEBUG`).

Run `python chatbot.py --help` to see the full list of options.

## Troubleshooting

- **`pyaudio` fails to install**: Confirm PortAudio is installed and accessible. On Windows ensure that Visual C++ Build Tools
  are available.
- **Wake word not detected**: Increase `--ambient-noise-duration` to allow for longer calibration or decrease background noise.
- **No response from OpenAI**: Verify network connectivity and that the API key is valid and has the required model access.
- **Audio playback issues**: `playsound` uses the system default player. If playback is unreliable, consider replacing it with a
  platform-specific alternative during training exercises.

## Contributing

This codebase is intentionally small so it can be modified during workshops. Issues and pull requests that improve clarity,
reliability, or pedagogical value are welcome.
