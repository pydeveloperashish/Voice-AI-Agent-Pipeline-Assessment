class TTSStub:

    def synthesize(self, text: str):

        # Simulate generating speech from text
        return {
            "audio_generated": False,
            "message": "TTS generation simulated",
            "text_response": text
        }