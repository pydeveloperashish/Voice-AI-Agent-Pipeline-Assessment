from orchestrator.pipeline import VoicePipeline
from stt.transcribe_stt import TranscribeSTT
from llm.process_llm import QuerySolving
from llm.llm_models import OpenAILLM, OllamaLLM
from stt.stt_models import WhisperSTT
from tts_stub.tts_stub import TTSStub
import json
import os
import sys

DEFAULT_AUDIOFILE = os.path.join(os.path.dirname(__file__), "sample_audio", "audio.m4a")


def main():
    # Check if audio file was passed via CLI
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = DEFAULT_AUDIOFILE

    stt = WhisperSTT('tiny')
    stt_service = TranscribeSTT(stt)

    # You can use OpenAILLM below, make sure to give openai api key in .env to use OpenAILLM
    llm_model = OllamaLLM()      
    query_solving_service = QuerySolving(llm_model)
    
    tts_stub_service = TTSStub()

    voice_pipeline = VoicePipeline(stt_service, query_solving_service, tts_stub_service)
    result = voice_pipeline.run(audio_file)

    print('\n')
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()