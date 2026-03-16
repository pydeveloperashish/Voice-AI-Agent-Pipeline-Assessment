# Voice Agent Pipeline (STT → LLM → Structured Output)

This project implements a **minimal voice agent pipeline** that
processes a spoken user request, interprets it using an LLM, and returns
a structured response.

The system simulates the core components of a voice agent:

Audio → Speech-to-Text → LLM Reasoning → Structured Output → (Stubbed
TTS)

------------------------------------------------------------------------

# How to Run the Project

## 1. Clone the repository

``` bash
git clone https://github.com/pydeveloperashish/Voice-AI-Agent-Pipeline-Assessment.git
cd Voice-AI-Agent-Pipeline-Assessment
```

## 2. Create environment and install dependencies

``` bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. (Optional) Install Ollama and pull a local model

If using local models for LLM generation:

``` bash
ollama pull lfm2.5-thinking:latest
```

## 4. Run the pipeline

``` bash
python main.py sample_audio/audio.m4a
```

The pipeline will: 1. Transcribe the audio file 2. Analyze the request
using an LLM 3. Return structured output 4. Simulate a TTS step

------------------------------------------------------------------------

# Example Output

``` json
{
  "stt": {
    "transcript": " Help me. I cannot access my account. I think I forgot my password. Can you help me with this?",
    "language": "en"
  },
  "llm": {
    "intent": "password_reset",
    "action": "reset_password",
    "confidence": 1.0,
    "notes": "User requested assistance with password reset."
  },
  "tts": {
    "audio_generated": false,
    "message": "TTS generation simulated",
    "text_response": "User requested assistance with password reset."
  },
  "latency": {
    "stt_seconds": 0.826,
    "llm_seconds": 6.033,
    "total_seconds": 6.862
  }
}
```

------------------------------------------------------------------------

# Key Design Decisions

## Modular Pipeline Architecture

Each major component is separated:

STT → LLM Reasoning → Pipeline Orchestration → TTS

This allows components to be swapped independently without modifying the
pipeline.

Examples:

-   STT can be replaced with Deepgram or AssemblyAI
-   LLM can be replaced with OpenAI or local models
-   TTS can be replaced with real speech synthesis engines

------------------------------------------------------------------------

## Dependency Injection

The pipeline receives **services instead of concrete implementations**.

Example:

``` python
VoicePipeline(stt_service, llm_service)
```

This keeps the orchestration logic independent from specific model
implementations.


------------------------------------------------------------------------

## Open--Closed Principle

The system follows the **Open--Closed Principle (OCP)**:

> Software entities should be open for extension but closed for
> modification.

### LLM Layer

A base abstraction is defined:

    BaseLLM

Concrete implementations extend it:

    OpenAILLM
    OllamaLLM

Adding a new model requires **creating a new class that extends
`BaseLLM`**, without modifying existing pipeline logic.

Example future extension:

    class ClaudeLLM(BaseLLM)
    class GeminiLLM(BaseLLM)

### STT Layer

Similarly, STT implementations follow the same pattern:

    BaseSTT
       ↓
    WhisperSTT

Future implementations could include:

    DeepgramSTT
    AssemblyAISTT

This design ensures the system is **easily extensible without modifying
existing code**.


------------------------------------------------------------------------

## Structured LLM Outputs

The LLM is instructed to return structured JSON with fields:

-   intent
-   action
-   confidence
-   notes

This makes the system easier to integrate with downstream automation.

------------------------------------------------------------------------

## Observability

The system includes:

-   step-level latency measurements
-   logging to console and file
-   structured outputs for easier debugging

------------------------------------------------------------------------

# Model Choices and Trade-offs

## Speech-to-Text: Whisper

The pipeline uses **OpenAI Whisper** for speech-to-text.

Reasons for choosing Whisper:

-   Open-source and runs locally
-   Strong multilingual transcription quality
-   Easy integration with Python

Trade-offs:

-   Slower inference when running on CPU
-   Cloud STT providers may offer lower latency and streaming support

Whisper was chosen because it provides a **good balance between
simplicity, reliability, and local execution**.

------------------------------------------------------------------------

## LLM: Local Ollama Model

The reasoning step uses a **local Ollama model**:

`lfm2.5-thinking:latest`

Reasons for choosing a local model:

-   Runs fully offline
-   No API cost
-   No external dependency
-   Reproducible environment

Trade-offs:

-   Smaller local models may produce weaker reasoning compared to large
    hosted models
-   JSON output may occasionally require validation or fallback handling

------------------------------------------------------------------------

## Optional OpenAI Integration

The pipeline is designed so the LLM provider can be easily swapped.

To use OpenAI instead of a local model:

1.  Add an API key in `.env`

```{=html}
<!-- -->
```
    OPENAI_API_KEY=your_key_here

2.  Update `main.py`:

``` python
llm_model = OpenAILLM()
```

No other code changes are required.

------------------------------------------------------------------------

# Where Things Might Break

## STT Errors

Speech recognition may fail due to:

-   noisy environments
-   poor audio quality
-   accents or unclear speech

This directly affects downstream reasoning.

------------------------------------------------------------------------

## LLM Output Variability

LLMs may occasionally return:

-   malformed JSON
-   incorrect confidence values
-   ambiguous intent classifications

The pipeline includes fallback handling to reduce crashes.

------------------------------------------------------------------------

## Model Performance

Local models may produce weaker reasoning compared to large hosted
models.

------------------------------------------------------------------------

## Latency Variability

Latency may vary depending on:

-   CPU vs GPU hardware
-   model size
-   local vs remote inference

------------------------------------------------------------------------

# Evaluation and Regression Testing

A small labeled dataset of audio samples could be maintained.

Example:

  Audio                  Expected Intent
  ---------------------- -----------------
  reset_password.wav     reset_password
  billing_question.wav   billing_support

Evaluation process:

1.  Run pipeline on test dataset
2.  Compare predicted intent vs expected intent
3.  Track metrics such as accuracy and confidence distribution

This allows detection of regressions when prompts or models change.


------------------------------------------------------------------------

# What I Would Improve With More Time

- Streaming Voice Processing
- Stronger Structured Output Validation
- Better Error Handling
- Evaluation Framework
- Real TTS Integration

------------------------------------------------------------------------

# Tech Stack

-   Python
-   Whisper STT
-   Ollama LLM
-   Logging and latency tracking
-   Modular service-based architecture
