
class BaseSTT:
    def transcribe(self, prompt: str) -> dict:
        raise NotImplementedError
    

# Openai Openai-Whisper-STT Implementation
import whisper
class WhisperSTT(BaseSTT):
    def __init__(self, model_name):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result
