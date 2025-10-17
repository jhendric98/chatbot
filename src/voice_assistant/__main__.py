"""Entry point for running voice assistant as a module: python -m voice_assistant"""
import sys

from voice_assistant.cli import main

if __name__ == "__main__":
    sys.exit(main())

