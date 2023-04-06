# Voice Assistant with GPT-3.5
This is a voice assistant application that listens for a voice command, transcribes it, generates a response using the OpenAI GPT-3.5 model, and speaks the response using a text-to-speech engine. The application is built using Python and several libraries such as openai, pyttsx3, speech_recognition, pyaudio, and google.

## Overview
The voice assistant continuously listens for the keyword "Genius" to start the process. Once it detects the keyword, it records the user's question, transcribes it, generates a response using the GPT-3.5 model, and speaks the response using the text-to-speech engine. The script then resumes listening for the keyword to repeat the process.


## Class Explanation
### VoiceAssistant
The VoiceAssistant class is the core class of the application. It contains methods for transcribing audio, generating a response using the GPT-3.5 model, speaking the text using the text-to-speech engine, and recording audio from the user.

Methods in the VoiceAssistant class:
- `__init__()`: Initializes the instance with the API key and necessary objects.
- `transcribe_audio_to_text(filename)`: Transcribes the audio file to text using the Google Speech Recognition API.
- `generate_response(prompt)`: Generates a response from the GPT-3.5 model using the OpenAI API.
- `speak_text(text)`: Speaks the given text using the text-to-speech engine.
- `record_audio(source)`: Records audio from the user using the microphone.
- `main()`: The main method that controls the flow of the application.

## Instructions for Use

1. Install the required libraries:
```
pip install openai pyttsx3 SpeechRecognition pyaudio google
```
2. Set up an OpenAI API key and add it to the api_key.py file:
```
API_KEY = "your_openai_api_key_here"
```
3. Run the script:
```
python chatbot.py
```
4. Say "Genius" to start recording your question. The application will transcribe your question, generate a response using the GPT-3.5 model, and speak the response using the text-to-speech engine.
5. The script will continue listening for the keyword "Genius" to repeat the process.

### Note: Make sure you have a working microphone connected to your computer.