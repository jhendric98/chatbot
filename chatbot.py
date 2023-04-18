# Description: This is a simple chatbot that uses the OpenAI API to generate responses to user questions.
import openai
import pyttsx3
import speech_recognition as sr
import time
import pyaudio
from api_key import API_KEY


class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant."""
        self.api_key = API_KEY
        self.openai = openai
        self.openai.api_key = self.api_key
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def transcribe_audio_to_text(self, filename):
        """Transcribe the audio file to text."""
        with sr.AudioFile(filename) as source:
            audio = self.recognizer.record(source)
        try:
            return self.recognizer.recognize_google(audio)
        except:
            print("Skipping unknown error")

    def generate_response(self, prompt):
        """Generate a response from the GPT-3.5 model using the OpenAI API."""
        response = self.openai.Completion.create(
            engine="chatgpt3.5",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["text"]

    def speak_text(self, text):
        """Speak the given text using the text-to-speech engine."""
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, source):
        """Record audio from the user."""
        audio = self.recognizer.listen(source)
        return audio

    def main(self):
        """Run the main loop of the voice assistant."""
        while True:
            print("Say 'Genius' to start recording your question")
            with sr.Microphone() as source:
                audio = self.record_audio(source)
                try:
                    transcription = self.recognizer.recognize_google(audio)
                    if transcription.lower() == "genius":
                        filename = "input.wav"
                        print("Say your question....")
                        with sr.Microphone() as source:
                            self.recognizer.pause_threshold = 1
                            audio = self.record_audio(source)
                            with open(filename, "wb") as f:
                                f.write(audio.get_wav_data())

                        text = self.transcribe_audio_to_text(filename)
                        if text:
                            print(f"You said: {text}")
                            response = self.generate_response(text)
                            print(f"GPT-3.5 says: {response}")
                            self.speak_text(response)

                except Exception as e:
                    print("An error occurred: {}".format(e))


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.main()
