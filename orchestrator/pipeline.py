"""pipeline.py is the orchestrator, so it should only:

Call STT
Validate transcript
Call LLM reasoning
Apply fallback logic
Return final structured output

It should NOT contain STT or LLM implementation code."""


from utils.logger import get_logger
logger = get_logger(__name__)

class VoicePipeline:

    def __init__(self, stt_service, llm_service):
        """
        stt_service: TranscribeSTT Object
        llm_service: request understanding Object
        """
        self.stt = stt_service
        self.llm = llm_service
        logger.info("Starting voice pipeline")

    def run(self, audio_path: str) -> dict:
        """
        Executes the full voice pipeline.
        """

        # Step 1: Speech-to-text
        logger.info("Running STT Transcribe step")
        stt_result = self.stt.transcribe(audio_path)
        logger.info(f"Detected language: {stt_result["language"]}")

        transcript = stt_result['transcript']

        if not transcript:
            return {
                "error": "No speech detected",
            }
        logger.info("STT Transcribe completed")

        # Step 2: LLM reasoning
        logger.info("Running LLM Reasoning")
        analysis = self.llm.analyze(transcript)

        logger.info(f"Intent: {analysis.get('intent')} | Confidence: {analysis.get('confidence')}")
        logger.info(f"Action: {analysis.get('action')}")

        # Step 3: Basic confidence fallback
        if analysis.get("confidence", 0) < 0.4:
            analysis["intent"] = "unclear"
            analysis["action"] = "unclear"
            analysis["notes"] = "Low confidence prediction"
        
        logger.info("LLM Reasoning completed")

        # Step 4: Return final structured output
        logger.info("Pipeline completed")
        return {
            "stt": stt_result,
            "llm": analysis
        }
    
  