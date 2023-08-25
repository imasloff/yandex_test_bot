import speech_recognition as sr
import subprocess
import os


class VoiceConverter:

    def __init__(self, filename: str, lang: str = 'ru-RU') -> None:
        self.lang = lang
        subprocess.run(['ffmpeg', '-v', 'quiet', '-i', filename,
                       filename.replace('.ogg', '.wav')],  shell=True)
        self.wav_file = filename.replace('.ogg', '.wav')

    def audio2text(self) -> str:
        recognizer = sr.Recognizer()

        with sr.AudioFile(self.wav_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=self.lang)

    def __del__(self):
        os.remove(self.wav_file)