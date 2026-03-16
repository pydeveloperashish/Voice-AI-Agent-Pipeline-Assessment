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
git clone <repo_url>
cd voice-agent-pipeline
```

## 2. Create environment and install dependencies

``` bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. (Optional) Install Ollama and pull a local model

If using local models:

``` bash
ollama pull llama3
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
    "transcript": "I forgot my password and cannot access my account",
    "language": "en"
  },
  "llm": {
    "intent": "reset_password",
    "action": "reset_password",
    "confidence": 0.91,
    "notes": "User requested help resetting their password."
  },
  "latency": {
    "stt_seconds": 2.34,
    "llm_seconds": 0.71,
    "total_seconds": 3.05
  }
}
```

------------------------------------------------------------------------

# Key Design Decisions

## Modular Pipeline Architecture

Each major component is isolated:

STT → LLM Reasoning → Pipeline Orchestration

This allows components to be swapped independently.

Examples: - STT can be replaced with Deepgram or AssemblyAI - LLM can be
replaced with OpenAI or local Ollama models

## Dependency Injection

The pipeline receives **services rather than concrete implementations**.

Example:

``` python
VoicePipeline(stt_service, llm_service)
```

This keeps the pipeline independent of low-level implementations.

## Structured LLM Outputs

The LLM is instructed to return JSON with fields:

-   intent
-   action
-   confidence
-   notes

This allows downstream systems to easily consume the output.

## Robustness

Basic safeguards were implemented:

-   fallback for low confidence predictions
-   JSON parsing error handling
-   confidence normalization
-   validation of transcript output

## Observability

The pipeline includes:

-   step-level latency measurements
-   logging to console and file
-   clear structured outputs

------------------------------------------------------------------------

# Where Things Might Break

## STT Errors

Speech-to-text models may produce incorrect transcripts due to:

-   background noise
-   poor audio quality
-   accents or speech patterns

This directly affects downstream reasoning.

## LLM Output Variability

LLMs may occasionally return:

-   malformed JSON
-   incorrect confidence values
-   ambiguous intent classifications

The pipeline includes fallback handling but cannot guarantee perfect
outputs.

## Model Performance

Local models (e.g., lfm2.5-thinking:latest) may produce weaker reasoning compared to
larger hosted models.

## Latency Variability

STT and LLM inference times may vary depending on:

-   hardware
-   model size
-   network latency (for API models)

------------------------------------------------------------------------

# Evaluation and Regression Testing

To evaluate the pipeline, a small labeled dataset of audio samples could
be maintained.

Example:

  Audio                  Expected Intent
  ---------------------- -----------------
  reset_password.wav     reset_password
  billing_question.wav   billing_support

The pipeline could be run against this dataset and results compared with
expected outputs to track accuracy and detect regressions.

------------------------------------------------------------------------

# What I Would Improve With More Time

## Streaming Audio Processing

Support real-time speech processing using WebRTC or streaming STT.

## Structured Output Enforcement

Use stricter schema validation to ensure LLM responses always follow the
expected format.

## Improved Error Handling

Add retry strategies and stronger validation for LLM responses.

## Evaluation Framework

Introduce automated regression testing with a labeled dataset and
performance metrics.

## Real TTS Integration

Replace the stubbed TTS component with a real speech synthesis engine
(e.g., ElevenLabs, Amazon Polly).

------------------------------------------------------------------------

# Tech Stack

-   Python
-   OpenAI / Ollama
-   Whisper STT
-   Python logging
-   Modular service-based architecture
