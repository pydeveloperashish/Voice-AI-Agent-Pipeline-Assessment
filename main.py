from orchestrator.pipeline import VoicePipeline
from stt.transcribe_stt import TranscribeSTT
from llm.process_llm import QuerySolving
from llm.llm_models import OpenAILLM, OllamaLLM
from stt.stt_models import WhisperSTT
import os


AUDIOFILE = os.path.join(os.path.dirname(__file__), "sample_audio", "audio.m4a")

stt = WhisperSTT('tiny')
stt_service = TranscribeSTT(stt)
llm_model = OllamaLLM()
query_solving_service = QuerySolving(llm_model)

voice_pipeline = VoicePipeline(stt_service, query_solving_service)
result = voice_pipeline.run(AUDIOFILE)
print("stt output: ", result['stt'])
print("llm output: ", result['llm'])