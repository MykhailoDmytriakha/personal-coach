from openai import OpenAI
from ..utils.config import get_config

class Transcriber:
    def __init__(self, api_key=None, language=None):
        config = get_config()
        self.client = OpenAI(api_key=api_key or config['openai_api_key'])
        self.model = config.get('openai_whisper_model', 'whisper-1')
        self.language = language or config.get('default_language', 'en')

    def transcribe(self, audio_file, language=None):
        try:
            with open(audio_file, "rb") as file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=file,
                    response_format="text",
                    language=language or self.language
                )
            return transcript
        except Exception as e:
            print(f"Transcription Error: {e}")
            return ""

    def set_language(self, language):
        self.language = language