from .llm_models import BaseLLM

class QuerySolving:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def analyze(self, transcript: str):

        prompt = f"""
Return ONLY JSON.

Fields:
intent
action
confidence
notes

Possible actions:
- reset_password
- billing_support
- technical_support
- general_question
- unclear

User transcript:
{transcript}
"""
        result = self.llm.generate(prompt)
        confidence = result.get("confidence", 0)

        try:
            result["confidence"] = float(confidence)
        except (ValueError, TypeError):
            result["confidence"] = 0.0

        return result
    




if __name__ == "__main__":

    from .llm_models import OpenAILLM, OllamaLLM

    model = OllamaLLM()

    query_solving_service = QuerySolving(model)

    result = query_solving_service.analyze(
        "I forgot my password and cannot login"
    )

    print(result)