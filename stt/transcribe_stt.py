import os
import sys

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

    DEFAULT_AUDIOFILE = os.path.join(os.getcwd(), "sample_audio", "audio.m4a")
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = DEFAULT_AUDIOFILE

    stt = WhisperSTT("tiny")
    stt_service = TranscribeSTT(stt)
    result = stt_service.transcribe(audio_file)
    print(f"Transcribed Text: {result['transcript']}")
    print(f"Language: {result['language']}")