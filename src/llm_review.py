import openai
from src.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def review_code_with_llm(code_diff):
    """Sends code changes to LLM for review."""
    prompt = f"Review the following GitHub pull request diff:\n{code_diff}\nProvide improvements and security suggestions."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
