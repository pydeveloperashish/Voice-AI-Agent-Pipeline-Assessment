"""pipeline.py is the orchestrator, so it should only:

Call STT
Validate transcript
Call LLM reasoning
Apply fallback logic
Return final structured output

It should NOT contain STT or LLM implementation code."""


class VoicePipeline:

    def __init__(self, stt_service, llm_service):
        """
        stt_service: TranscribeSTT Object
        llm_service: request understanding Object
        """
        self.stt = stt_service
        self.llm = llm_service

    def run(self, audio_path: str) -> dict:
        """
        Executes the full voice pipeline.
        """

        # Step 1: Speech-to-text
        stt_result = self.stt.transcribe(audio_path)

        transcript = stt_result['transcript']

        if not transcript:
            return {
                "error": "No speech detected",
            }

        # Step 2: LLM reasoning
        analysis = self.llm.analyze(transcript)

        # Step 3: Basic confidence fallback
        if analysis.get("confidence", 0) < 0.4:
            analysis["intent"] = "unclear"
            analysis["action"] = "unclear"
            analysis["notes"] = "Low confidence prediction"

        # Step 4: Return final structured output
        return {
            "stt": stt_result,
            "llm": analysis
        }
    
  