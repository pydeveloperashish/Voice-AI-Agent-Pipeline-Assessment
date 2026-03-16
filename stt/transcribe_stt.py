import os

class TranscribeSTT:
    def __init__(self, stt):
        self.stt = stt

    def transcribe(self, audio_path):
        result = self.stt.transcribe(audio_path)
        output = {
            "transcript": result["text"],
            "language": result["language"]
        }
        return output



if __name__ == "__main__":
    from stt_models import WhisperSTT

    AUDIOFILE = os.path.join(os.path.dirname(__file__), "sample_audio", "audio.m4a")
    stt = WhisperSTT("tiny")
    stt_service = TranscribeSTT(stt)
    result = stt_service.transcribe(AUDIOFILE)
    print(f"Transcribed Text: {result['text']}")
    print(f"Language: {result['language']}")