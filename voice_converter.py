import speech_recognition as sr
import subprocess
import os


class VoiceConverter:

    def __init__(self, filename: str, lang: str = 'ru-RU') -> None:
        self.lang = lang
        cmd = ' '.join(['ffmpeg', '-v', 'quiet', '-i', filename,
                       filename.replace(".ogg", ".wav")])
        subprocess.call(cmd, cwd=os.getcwd(), shell=True)
        self.wav_file = filename.replace('.ogg', '.wav')

    def audio2text(self) -> str:
        recognizer = sr.Recognizer()

        with sr.AudioFile(self.wav_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=self.lang)

    def __del__(self):
        os.remove(self.wav_file)
